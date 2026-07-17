# # apps/timetable/models.py
# # Developed by SAYAB

# from django.db import models
# from apps.courses.models import Course
# from apps.users.models import Teacher, Student

# DAYS_OF_WEEK = (
#     ('Monday', 'Monday'),
#     ('Tuesday', 'Tuesday'),
#     ('Wednesday', 'Wednesday'),
#     ('Thursday', 'Thursday'),
#     ('Friday', 'Friday'),
#     ('Saturday', 'Saturday'),
# )

# class TimeSlot(models.Model):
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     def __str__(self):
#         return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

# class TimetableEntry(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
#     timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
#     room = models.CharField(max_length=50, blank=True, null=True)

#     def __str__(self):
#         return f"{self.course.name} - {self.day} - {self.timeslot}"

# class StudentTimetable(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     timetable_entry = models.ForeignKey(TimetableEntry, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('student', 'timetable_entry')  # prevent duplicate entries

#     def __str__(self):
#         return f"{self.student.user.username} - {self.timetable_entry}"


# File: backend/apps/timetable/models.py
# TimeSlot and schedule models (Developed by SAYAB)

from django.db import models
from django.conf import settings
from apps.courses.models import Course

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

class TimeSlot(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timeslots')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='teaching_slots')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.course.code} - {self.day} {self.start_time}"
