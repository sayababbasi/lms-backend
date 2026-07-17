# File: backend/apps/attendance/serializers.py
# Serializers for attendance (Developed by SAYAB)

from rest_framework import serializers
from .models import AttendanceRecord

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'student_name', 'course', 'course_title', 'date', 'present', 'status', 'created_at']

    def get_status(self, obj):
        return 'present' if obj.present else 'absent'

    def get_student_name(self, obj):
        if obj.student.first_name and obj.student.last_name:
            return f"{obj.student.first_name} {obj.student.last_name}"
        return obj.student.username
