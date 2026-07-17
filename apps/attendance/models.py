# # # # apps/attendance/models.py
# # # # Developed by SAYAB

# # # from django.db import models
# # # from apps.courses.models import Course
# # # from apps.users.models import Student, Teacher

# # # class Attendance(models.Model):
# # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# # #     date = models.DateField()
# # #     status = models.CharField(max_length=10, choices=(('Present','Present'), ('Absent','Absent')))

# # #     def __str__(self):
# # #         return f"{self.student.user.username} - {self.course.name} - {self.date}"

# # # apps/attendance/models.py
# # # Developed by SAYAB

# # from django.db import models
# # from apps.users.models import Student, Teacher
# # from apps.courses.models import Course

# # class Attendance(models.Model):
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# #     date = models.DateField()
# #     status = models.CharField(max_length=10, choices=(('Present','Present'), ('Absent','Absent')))

# #     def __str__(self):
# #         return f"{self.student.user.username} - {self.course.name} - {self.status}"


# # File: backend/apps/attendance/models.py
# # Attendance record model (Developed by SAYAB)

# from django.db import models
# from django.conf import settings
# from apps.courses.models import Course

# class AttendanceRecord(models.Model):
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance")
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     date = models.DateField()
#     present = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

# File: backend/apps/attendance/models.py
# Attendance records (Developed by SAYAB)

from django.db import models
from django.conf import settings
from apps.courses.models import Course

class AttendanceRecord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course', 'date']

    def __str__(self):
        return f"Attendance: {self.student} - {self.course} - {self.date}"
