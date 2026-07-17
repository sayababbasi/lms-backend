# # File: backend/apps/exams/serializers.py
# # Serializers for exams (Developed by SAYAB)

# from rest_framework import serializers
# from .models import Exam, Question, MCQOption

# class MCQOptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MCQOption
#         fields = "__all__"

# class QuestionSerializer(serializers.ModelSerializer):
#     options = MCQOptionSerializer(many=True, read_only=True)
#     class Meta:
#         model = Question
#         fields = "__all__"

# class ExamSerializer(serializers.ModelSerializer):
#     questions = QuestionSerializer(many=True, read_only=True)
#     class Meta:
#         model = Exam
#         fields = "__all__"

# File: backend/apps/exams/serializers.py
# Serializers for exams (Developed by SAYAB)

from rest_framework import serializers
from .models import Exam, Question, MCQOption, ExamAttempt, ExamAnswer

class MCQOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQOption
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    options = MCQOptionSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = "__all__"

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    has_attempted = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = "__all__"

    def get_has_attempted(self, obj):
        user = self.context.get('request').user if 'request' in self.context else None
        if user and not user.is_anonymous:
            return ExamAttempt.objects.filter(student=user, exam=obj).exists()
        return False

class ExamAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    correct_option_text = serializers.SerializerMethodField()
    selected_option_text = serializers.CharField(source='selected_option.text', read_only=True, allow_null=True)
    
    class Meta:
        model = ExamAnswer
        fields = "__all__"

    def get_correct_option_text(self, obj):
        correct_opt = obj.question.options.filter(is_correct=True).first()
        return correct_opt.text if correct_opt else None

class ExamAttemptSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    course_name = serializers.CharField(source='exam.course.title', read_only=True)
    total_marks = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    answers = ExamAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = ExamAttempt
        fields = "__all__"

    def get_total_marks(self, obj):
        return sum(q.marks for q in obj.exam.questions.all())

    def get_total_questions(self, obj):
        return obj.exam.questions.count()

class ExamAnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField(required=False, allow_null=True)
    text_answer = serializers.CharField(required=False, allow_blank=True)

class ExamSubmissionSerializer(serializers.Serializer):
    answers = ExamAnswerSubmissionSerializer(many=True)
