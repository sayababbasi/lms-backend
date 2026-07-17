# File: backend/apps/timetable/serializers.py
# Serializers for timetable (Developed by SAYAB)

from rest_framework import serializers
from .models import TimeSlot

class TimeSlotSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    teacher_name = serializers.SerializerMethodField()
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')

    class Meta:
        model = TimeSlot
        fields = ['id', 'course', 'course_title', 'teacher', 'teacher_name', 'day', 'start_time', 'end_time', 'room_number']

    def get_teacher_name(self, obj):
        if obj.teacher:
            return f"{obj.teacher.first_name} {obj.teacher.last_name}"
        return "TBA"
