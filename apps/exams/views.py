# # from django.http import JsonResponse

# # def dummy_view(request):
# #     return JsonResponse({"message": "Exams app is working"})
# # File: backend/apps/exams/views.py
# # Minimal viewsets for exams (Developed by SAYAB)

# from rest_framework import viewsets
# from .models import Exam, Question, MCQOption
# from .serializers import ExamSerializer, QuestionSerializer, MCQOptionSerializer

# class ExamViewSet(viewsets.ModelViewSet):
#     queryset = Exam.objects.all()
#     serializer_class = ExamSerializer

# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

# class MCQOptionViewSet(viewsets.ModelViewSet):
#     queryset = MCQOption.objects.all()
#     serializer_class = MCQOptionSerializer


# File: backend/apps/exams/views.py
# Viewsets for exams (Developed by SAYAB)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exam, Question, MCQOption, AdmitCard
from .serializers import ExamSerializer, QuestionSerializer, MCQOptionSerializer
from apps.attendance.models import AttendanceRecord
import uuid

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    @action(detail=True, methods=['get'])
    def check_eligibility(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        
        target_student = user
        
        # If admin/teacher checking for a specific student
        if 'student_id' in request.query_params:
             if user.is_teacher or user.is_staff:
                 try:
                     from django.contrib.auth import get_user_model
                     User = get_user_model()
                     target_student = User.objects.get(pk=request.query_params['student_id'])
                 except User.DoesNotExist:
                     return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
             else:
                 return Response({'error': 'Unauthorized to check for others'}, status=status.HTTP_403_FORBIDDEN)

        if not hasattr(target_student, 'student_profile'):
             return Response({'error': 'user is not a student'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate Attendance
        total_sessions = AttendanceRecord.objects.filter(course=exam.course).values('date').distinct().count()
        present_count = AttendanceRecord.objects.filter(course=exam.course, student=target_student, present=True).count()
        
        percentage = 0
        if total_sessions > 0:
            percentage = (present_count / total_sessions) * 100
        
        eligible = percentage >= 80
        
        # Check if card already exists
        card_exists = AdmitCard.objects.filter(student=target_student, exam=exam).exists()
        
        return Response({
            'student': target_student.username,
            'eligible': eligible,
            'percentage': round(percentage, 1),
            'attended': present_count,
            'total': total_sessions,
            'card_exists': card_exists,
            'message': "Eligible for exam" if eligible else "Attendance low (<80%)"
        })

    @action(detail=True, methods=['post'])
    def generate_admit_card(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        target_student = user

        # Teacher/Admin generating for a student
        student_id = request.data.get('student_id')
        if student_id:
            if user.is_teacher or user.is_staff:
                try:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    target_student = User.objects.get(pk=student_id)
                except User.DoesNotExist:
                     return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if not hasattr(target_student, 'student_profile'):
             return Response({'error': 'User is not a student'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Check Eligibility again (Security)
        total_sessions = AttendanceRecord.objects.filter(course=exam.course).values('date').distinct().count()
        present_count = AttendanceRecord.objects.filter(course=exam.course, student=target_student, present=True).count()
        percentage = 0
        if total_sessions > 0:
            percentage = (present_count / total_sessions) * 100
            
        if percentage < 80:
             return Response({'error': 'Not eligible for admit card. Attendance < 80%.'}, status=status.HTTP_403_FORBIDDEN)
        
        # 2. Generate or Get Card
        card, created = AdmitCard.objects.get_or_create(
            student=target_student,
            exam=exam,
            defaults={
                'status': 'ISSUED',
                'unique_code': uuid.uuid4()
            }
        )
        
        if card.status == 'BLOCKED':
             return Response({'error': 'Admit card is blocked by admin.'}, status=status.HTTP_403_FORBIDDEN)
             
        return Response({
            'status': 'success',
            'admit_card': {
                'id': card.id,
                'student_name': f"{target_student.first_name} {target_student.last_name}",
                'exam_title': exam.title,
                'course': exam.course.title,
                'unique_code': card.unique_code,
                'generated_at': card.generated_at
            }
        })

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class MCQOptionViewSet(viewsets.ModelViewSet):
    queryset = MCQOption.objects.all()
    serializer_class = MCQOptionSerializer

from .models import ExamAttempt, ExamAnswer
from .serializers import ExamAttemptSerializer, ExamSubmissionSerializer
from django.utils import timezone

class StudentExamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [] # TODO: Add IsStudent permission

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'student_profile'):
            return Exam.objects.none()
        
        # Determine active exams (example logic)
        # For now return all exams from enrolled courses
        student_profile = user.student_profile
        from apps.courses.models import Course
        enrolled_courses = Course.objects.filter(students=student_profile)
        return Exam.objects.filter(course__in=enrolled_courses).order_by('start_time')

    @action(detail=False, methods=['get'])
    def my_results(self, request):
        user = request.user
        attempts = ExamAttempt.objects.filter(student=user, submit_time__isnull=False).order_by('-submit_time')
        serializer = ExamAttemptSerializer(attempts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def result_detail(self, request):
        attempt_id = request.query_params.get('attempt_id')
        if not attempt_id:
            return Response({'error': 'attempt_id required'}, status=400)
        
        try:
            attempt = ExamAttempt.objects.get(id=attempt_id, student=request.user)
            serializer = ExamAttemptSerializer(attempt)
            return Response(serializer.data)
        except ExamAttempt.DoesNotExist:
            return Response({'error': 'Result not found'}, status=404)

    @action(detail=True, methods=['post'])
    def start_attempt(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        
        # diverse checks could go here (e.g. admit card existence)
        
        # Check if already attempted
        existing_attempt = ExamAttempt.objects.filter(student=user, exam=exam).first()
        if existing_attempt:
             return Response(ExamAttemptSerializer(existing_attempt).data)
        
        attempt = ExamAttempt.objects.create(student=user, exam=exam)
        return Response(ExamAttemptSerializer(attempt).data)

    @action(detail=True, methods=['post'])
    def submit_exam(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        
        attempt = ExamAttempt.objects.filter(student=user, exam=exam).first()
        if not attempt:
            return Response({'error': 'No active attempt found'}, status=status.HTTP_400_BAD_REQUEST)
            
        if attempt.submit_time:
             return Response({'error': 'Exam already submitted'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle multipart form data
        import json
        answers_data = []
        if 'answers_data' in request.data:
            try:
                answers_data = json.loads(request.data.get('answers_data', '[]'))
            except json.JSONDecodeError:
                return Response({'error': 'Invalid answers_data JSON'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ExamSubmissionSerializer(data=request.data)
            if serializer.is_valid():
                answers_data = serializer.validated_data.get('answers', [])
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        total_score = 0
        
        for ans_data in answers_data:
            q_id = ans_data.get('question_id')
            selected_opt_id = ans_data.get('selected_option_id')
            text_answer = ans_data.get('text_answer', '')
            
            try:
                question = Question.objects.get(id=q_id, exam=exam)
                marks = 0
                selected_option = None
                file_obj = request.FILES.get(f'file_{q_id}')
                
                if question.question_type == 'MCQ' and selected_opt_id:
                    selected_option = MCQOption.objects.get(id=selected_opt_id, question=question)
                    if selected_option.is_correct:
                        marks = question.marks
                        
                # Text answer and file answer are typically graded manually later, 
                # so we don't automatically award marks here unless it's MCQ.
                        
                ExamAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=selected_option,
                    text_answer=text_answer,
                    file_answer=file_obj,
                    marks_awarded=marks
                )
                total_score += marks
                
            except (Question.DoesNotExist, MCQOption.DoesNotExist):
                continue
        
        attempt.score = total_score
        attempt.submit_time = timezone.now()
        attempt.save()
        
        return Response({
            'status': 'submitted',
            'score': total_score,
            'attempt_id': attempt.id
        })
