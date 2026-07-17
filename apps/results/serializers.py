# # File: backend/apps/results/serializers.py
# # Serializers for results (Developed by SAYAB)

# from rest_framework import serializers
# from .models import Result

# class ResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Result
#         fields = "__all__"


# File: backend/apps/results/serializers.py
# Serializers for results (Developed by SAYAB)

from rest_framework import serializers
from .models import Result, Transcript

class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    exam_title = serializers.CharField(source='course.code', read_only=True) # Fallback if no specific exam model linked directly in this view

    class Meta:
        model = Result
        fields = ['id', 'student', 'student_name', 'course', 'course_title', 'exam_title', 'marks_obtained', 'total_marks', 'grade', 'is_blocked', 'comments', 'published', 'created_at']

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = "__all__"
