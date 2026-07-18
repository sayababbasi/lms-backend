from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Course, Module, Lesson, Resource, EnrollmentRequest
from .serializers import (
    CourseSerializer, 
    CourseListSerializer, 
    ModuleSerializer, 
    LessonSerializer, 
    ResourceSerializer,
    EnrollmentRequestSerializer
)
from apps.users.permissions import IsTeacher, IsAdmin
from rest_framework.views import APIView
from utils.email_service import EmailService

class StudentCoursesView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'student_profile'):
            return Course.objects.select_related('teacher').prefetch_related(
                'teachers', 'students'
            ).filter(students=user.student_profile)
        return Course.objects.none()

class CourseViewSet(viewsets.ModelViewSet):
    """
    Courses:
    - List: Public/Authenticated
    - Create/Update/Delete: Teacher/Admin only
    """
    queryset = Course.objects.none() # Required for DRF router basename
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
            
        from django.db.models import Q
        
        # Base optimization for all queries
        qs = Course.objects.select_related('teacher').prefetch_related(
            'teachers', 'students', 'modules__lessons__resources'
        ).order_by('-created_at')
        
        if user.is_staff or user.is_superuser:
            return qs
            
        if user.is_teacher:
            return qs.filter(
                Q(teacher=user) | Q(teachers=user)
            ).distinct()
            
        # Students might need to see the full catalog to enroll
        if user.is_student:
            return qs
            
        return Course.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'remove_student']:
            return [permissions.IsAuthenticated(), (IsTeacher | IsAdmin)()]
        return [permissions.IsAuthenticated()] # Students can view

    def perform_create(self, serializer):
        # Auto-assign teacher
        serializer.save(teacher=self.request.user)

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        if not student_id:
            return Response({'error': 'Student ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            student = get_user_model().objects.get(pk=student_id)
            if hasattr(student, 'student_profile'):
                 course.students.add(student.student_profile)
                 return Response({'status': 'Student added'})
            return Response({'error': 'User is not a student'}, status=status.HTTP_400_BAD_REQUEST)
        except get_user_model().DoesNotExist:
             return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        if not student_id:
            return Response({'error': 'Student ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            student = get_user_model().objects.get(pk=student_id)
            # Remove from M2M
            if hasattr(student, 'student_profile'):
                 course.students.remove(student.student_profile)
                 return Response({'status': 'Student removed'})
            return Response({'error': 'User is not a student'}, status=status.HTTP_400_BAD_REQUEST)
        except get_user_model().DoesNotExist:
             return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()

    def get_permissions(self):
        # Students can only read; teachers/admins can do full CRUD
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), (IsTeacher | IsAdmin)()]

    def get_queryset(self):
        qs = Module.objects.prefetch_related('lessons__resources').all()
        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), (IsTeacher | IsAdmin)()]

    def get_queryset(self):
        qs = Lesson.objects.prefetch_related('resources').all()
        module_id = self.request.query_params.get('module')
        if module_id:
            qs = qs.filter(module_id=module_id)
        return qs

    @action(detail=True, methods=['post'], url_path='delete-video')
    def delete_video(self, request, pk=None):
        """Remove the YouTube video from a lesson (clears video fields)."""
        lesson = self.get_object()
        lesson.youtube_video_id = None
        lesson.youtube_embed_url = None
        lesson.video_url = None
        lesson.upload_status = 'pending'
        lesson.video_duration = None
        lesson.uploaded_at = None
        lesson.save()
        return Response({'status': 'Video removed. You can now upload a new one.'})


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), (IsTeacher | IsAdmin)()]

    def get_queryset(self):
        qs = Resource.objects.all()
        lesson_id = self.request.query_params.get('lesson')
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)
        return qs

class EnrollmentRequestViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentRequest.objects.all()
    serializer_class = EnrollmentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = EnrollmentRequest.objects.all().order_by('-created_at')
        course_id = self.request.query_params.get('course', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            req = self.get_object()
            print(f"DEBUG: Approving Request {req.id} for Student {req.student.username}")
            
            if req.status != 'PENDING':
                return Response({'error': 'Request already processed'}, status=status.HTTP_400_BAD_REQUEST)
            
            req.status = 'APPROVED'
            req.save()
            
            # Add to course
            if hasattr(req.student, 'student_profile'):
                print(f"DEBUG: Adding student profile {req.student.student_profile.id} to course {req.course.code}")
                req.course.students.add(req.student.student_profile)
                EmailService.send_enrollment_notification(req.student, req.course, 'APPROVED')
                return Response({'status': 'Approved and enrolled'})
            
            print("DEBUG: User has NO student profile")
            return Response({'error': 'User has no student profile'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"DEBUG: Error approving request: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        req = self.get_object()
        if req.status != 'PENDING':
             return Response({'error': 'Request already processed'}, status=status.HTTP_400_BAD_REQUEST)

        req.status = 'REJECTED'
        req.save()
        EmailService.send_enrollment_notification(req.student, req.course, 'REJECTED')
        return Response({'status': 'Rejected'})
