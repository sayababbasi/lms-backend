from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.utils import timezone
from .models import Student, Teacher, Staff
from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, StaffSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent
from .services import PasswordService, AuthenticationService, AuditLogService, NotificationService
from utils.email_service import EmailService
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

# Custom Token Serializer to include user data
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        user = None
        try:
            # Django authenticate accepts either username or email depending on backend, 
            # simplejwt typically uses the USERNAME_FIELD
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                pass
                
        if user:
            if user.password_status == 'LOCKED':
                if user.locked_until and user.locked_until > timezone.now():
                    raise AuthenticationFailed("Account is locked due to too many failed attempts. Try again later.")
                elif user.locked_until and user.locked_until <= timezone.now():
                    user.password_status = 'ACTIVE'
                    user.failed_login_attempts = 0
                    user.locked_until = None
                    user.save()

        try:
            data = super().validate(attrs)
            if user:
                AuthenticationService.handle_successful_login(user)
                
            data['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'is_student': self.user.is_student,
                'is_teacher': self.user.is_teacher,
                'is_staff': self.user.is_staff,
                'force_password_change': self.user.force_password_change,
                'password_status': self.user.password_status
            }
            return data
        except Exception as e:
            if user:
                AuthenticationService.handle_failed_login(user)
            raise e

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Admin only viewset to manage all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin] 

    @action(detail=True, methods=['post'], url_path='generate-password')
    def generate_password(self, request, pk=None):
        user = self.get_object()
        password = PasswordService.generate_secure_password()
        is_valid, msg = PasswordService.validate_password_strength(password, user)
        if not is_valid:
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(password)
        user.password_status = 'TEMPORARY'
        user.force_password_change = True
        user.save()
        
        EmailService.send_welcome_email(user, password)
        
        PasswordService.record_password_history(user, password)
        AuditLogService.log_action(user=user, admin=request.user, action="Generated Temporary Password", ip_address=request.META.get('REMOTE_ADDR'))
        
        return Response({'temporary_password': password})

    @action(detail=True, methods=['post'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        user = self.get_object()
        password = request.data.get('password')
        
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        is_valid, msg = PasswordService.validate_password_strength(password, user)
        if not is_valid:
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(password)
        user.password_status = 'TEMPORARY' if request.data.get('is_temporary', False) else 'PERMANENT'
        user.force_password_change = request.data.get('force_change', False)
        user.save()
        
        EmailService.send_welcome_email(user, password)
        
        PasswordService.record_password_history(user, password)
        AuditLogService.log_action(user=user, admin=request.user, action="Password Reset by Admin", ip_address=request.META.get('REMOTE_ADDR'))
        
        return Response({'message': 'Password reset successfully.'})

    @action(detail=True, methods=['post'], url_path='force-password-change')
    def force_password_change(self, request, pk=None):
        user = self.get_object()
        user.force_password_change = True
        user.password_status = 'RESET_REQUIRED'
        user.save()
        
        AuditLogService.log_action(user=user, admin=request.user, action="Forced Password Change", ip_address=request.META.get('REMOTE_ADDR'))
        
        return Response({'message': 'User will be forced to change password on next login.'})

    @action(detail=True, methods=['get'], url_path='password-status')
    def password_status(self, request, pk=None):
        user = self.get_object()
        return Response({
            'status': user.password_status,
            'force_change': user.force_password_change,
            'last_changed': user.last_password_change,
            'failed_attempts': user.failed_login_attempts,
            'locked_until': user.locked_until
        })

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Student.objects.none()
            
        if user.is_staff:
            return Student.objects.all()
            
        if user.is_teacher:
            # Filter students enrolled in courses taught by this teacher
            from apps.courses.models import Course
            return Student.objects.filter(
                courses__in=Course.objects.filter(Q(teacher=user) | Q(teachers=user))
            ).distinct()
            
        if user.is_student:
            return Student.objects.filter(user=user)
            
        return Student.objects.none()

    def update(self, request, *args, **kwargs):
        print("PATCH request data:", request.data)
        try:
            response = super().update(request, *args, **kwargs)
            if response.status_code == 400:
                print("400 Error:", response.data)
            return response
        except Exception as e:
            print("Exception during update:", e)
            raise e

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdmin]

class MeView(APIView):
    """
    Get current authentication user profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class DashboardStatsView(APIView):
    """
    Get aggregated dashboard statistics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Imports here to avoid potential circular import issues depending on app loading order
        from apps.courses.models import Course
        from apps.assignments.models import Assignment
        
        # Active Students
        # Counting Student profiles where the associated User account is active
        active_students = Student.objects.filter(user__is_active=True).count()
        
        # Active Courses
        # Simple count for now
        active_courses = Course.objects.count()
        
        # Pending Assignments
        # For now, returning total count. Can be refined to assignments with future due dates.
        pending_assignments = Assignment.objects.count()
        
        # Total Revenue
        # Placeholder for now until Finance module is fully integrated
        total_revenue = 124500 

        data = {
            "total_students": active_students,
            "active_courses": active_courses,
            "pending_assignments": pending_assignments,
            "total_revenue": total_revenue
        }
        return Response(data)

class StudentStatsView(APIView):
    """
    Get aggregated dashboard statistics for a Student.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        print(f"DEBUG: StudentStatsView called by user: {user.username}")
        if not hasattr(user, 'student_profile'):
            print("DEBUG: User has no student_profile")
            return Response({"error": "User is not a student"}, status=403)
        
        student = user.student_profile
        print(f"DEBUG: derived student profile: {student.id}")

        # Imports to avoid circular imports
        from apps.courses.models import Course
        from apps.assignments.models import Assignment, Submission
        from apps.attendance.models import AttendanceRecord


        # 1. Active Courses (Enrollments)
        enrolled_courses = Course.objects.filter(students=student)
        enrolled_courses_count = enrolled_courses.count()
        print(f"DEBUG: Enrolled courses count: {enrolled_courses_count}")

        # 2. Pending Assignments
        enrolled_course_ids = enrolled_courses.values_list('id', flat=True)
        
        # Total assignments in these courses
        total_assignments = Assignment.objects.filter(course_id__in=enrolled_course_ids).count()
        
        # Submissions by this student
        submitted_assignments = Submission.objects.filter(
            student=user, 
            assignment__course_id__in=enrolled_course_ids
        ).count()
        
        pending_assignments = max(0, total_assignments - submitted_assignments)


        # 3. Attendance Percentage
        total_attendance_records = AttendanceRecord.objects.filter(student=user).count()
        present_count = AttendanceRecord.objects.filter(student=user, present=True).count()
        attendance_percentage = 0
        if total_attendance_records > 0:
            attendance_percentage = round((present_count / total_attendance_records) * 100, 2)

        # 4. CGPA (Placeholder)
        cgpa = "0.00"

        data = {
            "enrolled_courses": enrolled_courses_count,
            "pending_assignments": pending_assignments,
            "attendance": f"{attendance_percentage}%",
            "cgpa": cgpa
        }
        return Response(data)

class RegisterView(APIView):
    """
    Public registration endpoint.
    Creates user with is_active=False.
    Pending admin approval.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'student') # student or teacher

        if not username or not password or not email:
            return Response({"error": "Please provide username, email and password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create User (Active for Students to allow immediate payment, Inactive for Teachers)
        is_active = True if role == 'student' else False
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            is_active=is_active
        )

        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')

        # Handle Roles
        if role not in ['student', 'teacher']:
            return Response({"error": "Invalid role specified"}, status=status.HTTP_400_BAD_REQUEST)

        if role == 'teacher':
            user.is_teacher = True
            user.save()
            Teacher.objects.create(user=user, department="General") # Placeholder dept
        elif role == 'student':
            user.is_student = True
            user.save()
            # Generate temporary roll number
            import random
            roll_num = f"TEMP-{random.randint(1000, 9999)}"
            Student.objects.create(
                user=user, 
                roll_number=roll_num, 
                department="General"
            )
            EmailService.send_welcome_email(user)
        
        # Prepare Response
        res_data = {
            "message": "Registration successful. You can now login." if role == 'student' else "Registration successful. Please wait for admin approval.",
            "username": user.username,
            "status": "active" if role == 'student' else "pending"
        }

        # Auto-login for students
        if role == 'student':
            refresh = RefreshToken.for_user(user)
            res_data['access'] = str(refresh.access_token)
            res_data['refresh'] = str(refresh)
        
        return Response(res_data, status=status.HTTP_201_CREATED)

class PendingUsersView(APIView):
    """
    List all users pending approval (is_active=False).
    Admin only.
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        # Filter users who are inactive but not superusers/staff (unless staff also need approval)
        # Assuming we only want to approve students/teachers for now
        pending_users = User.objects.filter(is_active=False).exclude(is_superuser=True)
        serializer = UserSerializer(pending_users, many=True)
        return Response(serializer.data)

class ApproveUserView(APIView):
    """
    Approve a pending user.
    Sets is_active=True and simulating email sending.
    """
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_active:
            return Response({"message": "User is already active"}, status=status.HTTP_200_OK)
        
        user.is_active = True
        user.save()

        EmailService.send_welcome_email(user)

        return Response({"message": f"User {user.username} approved successfully"}, status=status.HTTP_200_OK)

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

class ForgotPasswordView(APIView):
    """
    Public endpoint to request a password reset email.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Assuming frontend will handle /reset-password/:uid/:token
            # Or use a generic lms URL
            reset_link = f"https://lms.revoticai.com/reset-password/{uid}/{token}"
            
            EmailService.send_password_reset(user, reset_link)
            
            # Record audit log
            AuditLogService.log_action(user=user, admin=None, action="Requested Password Reset", ip_address=request.META.get('REMOTE_ADDR'))
            
            return Response({"message": "If an account exists with that email, a reset link has been sent."})
        except User.DoesNotExist:
            # Still return success to prevent email enumeration
            return Response({"message": "If an account exists with that email, a reset link has been sent."})

class ResetPasswordConfirmView(APIView):
    """
    Public endpoint to confirm password reset using uid and token.
    """
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get('password')
        if not password:
            return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            is_valid, msg = PasswordService.validate_password_strength(password, user)
            if not is_valid:
                return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
                
            user.set_password(password)
            user.password_status = 'PERMANENT'
            user.force_password_change = False
            user.save()
            
            PasswordService.record_password_history(user, password)
            AuditLogService.log_action(user=user, admin=None, action="Completed Password Reset via Token", ip_address=request.META.get('REMOTE_ADDR'))
            
            return Response({"message": "Password has been reset successfully."})
        else:
            return Response({"error": "Invalid or expired reset token."}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    """
    Authenticated endpoint for a user to change their own password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({"error": "Both old and new passwords are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not user.check_password(old_password):
            return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)
            
        is_valid, msg = PasswordService.validate_password_strength(new_password, user)
        if not is_valid:
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(new_password)
        user.password_status = 'PERMANENT'
        user.force_password_change = False
        user.save()
        
        PasswordService.record_password_history(user, new_password)
        AuditLogService.log_action(user=user, admin=None, action="Changed Own Password", ip_address=request.META.get('REMOTE_ADDR'))
        
        return Response({"message": "Password changed successfully."})
