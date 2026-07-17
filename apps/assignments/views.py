from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django.conf import settings
from .models import Assignment, Submission, Grade
from apps.courses.models import Course
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSerializer
from apps.users.permissions import IsTeacher, IsStudent, IsAdmin

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    Assignments:
    - Teachers/Admins can create/edit.
    - Students can view.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        queryset = Assignment.objects.all().annotate(submissions_count=models.Count('submissions')).order_by('-created_at')
        course_id = self.request.query_params.get('course', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), (IsTeacher | IsAdmin)()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    Submissions:
    - Students create (submit).
    - Teachers view all for their assignments.
    """
    queryset = Submission.objects.all().order_by('-submitted_at')
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsStudent()]
        return [permissions.IsAuthenticated()] # Teachers verify list in get_queryset

    def get_queryset(self):
        user = self.request.user
        queryset = Submission.objects.all().order_by('-submitted_at')

        # Filter by assignment if provided
        assignment_id = self.request.query_params.get('assignment', None)
        if assignment_id:
            queryset = queryset.filter(assignment_id=assignment_id)

        if user.is_teacher or user.is_staff:
            return queryset
        return queryset.filter(student=user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class GradeViewSet(viewsets.ModelViewSet):
    """
    Grades:
    - Teachers create/update.
    - Students view only.
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), (IsTeacher | IsAdmin)()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class CourseAssignmentStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Statistics for Courses regarding Assignments and Quizzes.
    """
    permission_classes = [permissions.IsAuthenticated, (IsTeacher | IsAdmin)]

    def get_queryset(self):
        return Course.objects.all().annotate(
            assignments_count=models.Count('assignments', distinct=True),
            quizzes_count=models.Count('exams', distinct=True),
            submissions_count=models.Count('assignments__submissions', distinct=True),
            graded_submissions_count=models.Count('assignments__submissions', filter=models.Q(assignments__submissions__grade__isnull=False), distinct=True),
            average_grade=models.Avg('assignments__submissions__grade__score')
        )
    
    def get_serializer_class(self):
        from .serializers import CourseAssignmentStatsSerializer
        return CourseAssignmentStatsSerializer
class StudentAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(f"DEBUG: StudentAssignmentListView called by user: {user.username} (ID: {user.id})")
        
        if not hasattr(user, 'student_profile'):
             print("DEBUG: User has no student_profile")
             return Assignment.objects.none()
        
        student = user.student_profile
        # Filter assignments for enrolled courses
        # Using correct M2M relationship: Course.students
        # Student related name is 'courses' (implied or explicit)
        from apps.courses.models import Course
        enrolled_courses = Course.objects.filter(students=student)
        print(f"DEBUG: Enrolled courses count: {enrolled_courses.count()}")
        print(f"DEBUG: Enrolled course IDs: {list(enrolled_courses.values_list('id', flat=True))}")
        
        queryset = Assignment.objects.filter(course__in=enrolled_courses).order_by('due_date')
        print(f"DEBUG: Assignments found: {queryset.count()}")
        return queryset

class AssignmentSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        try:
            assignment = Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            return Response({'error': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check existing submission
        existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
        # Prepare data with assignment ID
        data = request.data.copy()
        data['assignment'] = pk

        if existing:
             serializer = SubmissionSerializer(existing, data=data, partial=True)
        else:
             serializer = SubmissionSerializer(data=data)

        if serializer.is_valid():
            submission = serializer.save(assignment=assignment, student=request.user)
            
            # Save uploaded file if present
            file_obj = request.FILES.get('file')
            if file_obj:
                from .models import SubmissionFile
                SubmissionFile.objects.create(
                    submission=submission,
                    file=file_obj,
                    filename=file_obj.name
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
