from rest_framework import serializers
from .models import (
    Assignment, AssignmentAttachment, Rubric, RubricCriteria,
    Submission, SubmissionFile, SubmissionComment, Grade
)
from apps.courses.models import Course

class AssignmentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentAttachment
        fields = ['id', 'file', 'filename', 'uploaded_at']

class RubricCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubricCriteria
        fields = ['id', 'title', 'description', 'max_points']

class RubricSerializer(serializers.ModelSerializer):
    criteria = RubricCriteriaSerializer(many=True, read_only=True)

    class Meta:
        model = Rubric
        fields = ['id', 'title', 'description', 'criteria', 'created_at']

class GradeSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'submission', 'teacher', 'teacher_name', 'score', 'rubric_score_data', 'feedback', 'private_notes', 'is_published', 'graded_at', 'updated_at']
        read_only_fields = ['teacher']

class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ['id', 'file', 'filename', 'uploaded_at']

class SubmissionCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = SubmissionComment
        fields = ['id', 'author', 'author_name', 'comment', 'created_at']
        read_only_fields = ['author']

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    grade = GradeSerializer(read_only=True)
    files = SubmissionFileSerializer(many=True, read_only=True)
    comments = SubmissionCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'student', 'student_name', 'status', 'attempt_number',
            'is_late', 'text_content', 'external_url', 'plagiarism_score',
            'submitted_at', 'created_at', 'updated_at', 'grade', 'files', 'comments'
        ]
        read_only_fields = ['student', 'status', 'is_late', 'plagiarism_score', 'submitted_at']

class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    submissions_count = serializers.IntegerField(read_only=True, required=False)
    
    attachments = AssignmentAttachmentSerializer(many=True, read_only=True)
    rubric = RubricSerializer(read_only=True)

    def get_submissions_count(self, obj):
        return getattr(obj, 'submissions_count', obj.submissions.count())

    is_submitted = serializers.SerializerMethodField()

    def get_is_submitted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.submissions.filter(student=request.user).exists()
        return False

    class Meta:
        model = Assignment
        fields = [
            'id', 'course', 'course_title', 'course_code', 'teacher', 'teacher_name',
            'title', 'description', 'instructions', 'max_score', 'passing_marks', 
            'weightage', 'assignment_type', 'publish_date', 'due_date', 'timezone',
            'submission_type', 'allow_resubmission', 'max_attempts', 'allow_late',
            'late_days_allowed', 'late_penalty_percentage', 'is_group_assignment',
            'anonymous_grading', 'peer_review', 'status', 'created_at', 'updated_at',
            'submissions_count', 'is_submitted', 'attachments', 'rubric'
        ]

class CourseAssignmentStatsSerializer(serializers.ModelSerializer):
    assignments_count = serializers.IntegerField(read_only=True)
    quizzes_count = serializers.IntegerField(read_only=True)
    submissions_count = serializers.IntegerField(read_only=True)
    graded_submissions_count = serializers.IntegerField(read_only=True)
    average_grade = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'assignments_count', 'quizzes_count', 'submissions_count', 'graded_submissions_count', 'average_grade']
