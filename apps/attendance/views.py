from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AttendanceRecord
from .serializers import AttendanceSerializer
from apps.users.permissions import IsTeacher, IsAdmin
from apps.courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bulk_update']:
            return [permissions.IsAuthenticated(), (IsTeacher | IsAdmin)()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course')
        date = self.request.query_params.get('date')
        
        student_id = self.request.query_params.get('student_id')
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if date:
            queryset = queryset.filter(date=date)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
            
        return queryset

    @action(detail=False, methods=['post'], url_path='bulk-update')
    def bulk_update(self, request):
        course_id = request.data.get('course')
        date = request.data.get('date')
        records = request.data.get('records') # List of {student_id, present}

        if not course_id or not date or records is None:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Process each record
        created_records = []
        for record in records:
            student_id = record.get('student_id')
            present = record.get('present')
            
            # Ensure unique constraint handling
            obj, created = AttendanceRecord.objects.update_or_create(
                student_id=student_id,
                course_id=course_id,
                date=date,
                defaults={'present': present}
            )
            created_records.append(obj)

        return Response({'status': 'success', 'updated': len(created_records)})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        course_id = request.query_params.get('course')
        if not course_id:
            return Response({'error': 'Course ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate stats
        total_sessions = AttendanceRecord.objects.filter(course_id=course_id).values('date').distinct().count()
        
        # Aggregate per student
        from django.db.models import Count, Q
        stats = AttendanceRecord.objects.filter(course_id=course_id).values('student').annotate(
            present_count=Count('id', filter=Q(present=True)),
            total_count=Count('id')
        )
        
        response_data = {
            'total_course_sessions': total_sessions,
            'student_stats': {
                s['student']: {
                    'present': s['present_count'],
                    'total': s['total_count'],
                    'percentage': round((s['present_count'] / s['total_count']) * 100, 1) if s['total_count'] > 0 else 0
                } for s in stats
            }
        }
        return Response(response_data)

    @action(detail=False, methods=['get'])
    def student_stats(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'Student ID required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = User.objects.get(pk=student_id)
        except User.DoesNotExist:
             return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all courses for this student
        # Assuming M2M relation is course.students (related_name='courses' on Student model?)
        # Let's check Course model. It has students = ManyToMany('users.Student', related_name='courses')
        # So student_profile.courses.all() gives courses.
        
        if not hasattr(student, 'student_profile'):
             return Response({'error': 'User is not a student'}, status=status.HTTP_400_BAD_REQUEST)

        courses = student.student_profile.courses.all()
        results = []

        from django.db.models import Count, Q

        for course in courses:
             # Total sessions for this course (unique dates)
             total_sessions = AttendanceRecord.objects.filter(course=course).values('date').distinct().count()
             
             # Student's attendance
             student_records = AttendanceRecord.objects.filter(course=course, student=student)
             present_count = student_records.filter(present=True).count()
             
             percentage = 0
             if total_sessions > 0:
                 percentage = round((present_count / total_sessions) * 100, 1)

             results.append({
                 'course_id': course.id,
                 'course_title': course.title,
                 'code': course.code,
                 'total_sessions': total_sessions,
                 'present_count': present_count,
                 'percentage': percentage,
                 'status': 'Eligible' if percentage >= 80 else 'Ineligible'
             })

        return Response({
            'student': {
                'id': student.id,
                'name': f"{student.first_name} {student.last_name}",
                'email': student.email,
                'roll_number': student.student_profile.roll_number
            },
            'courses': results
        })
