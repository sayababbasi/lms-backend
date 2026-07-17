# # # # # apps/results/models.py
# # # # # Developed by SAYAB

# # # # from django.db import models
# # # # from apps.users.models import Student
# # # # from apps.courses.models import Course

# # # # class Result(models.Model):
# # # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # # #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# # # #     marks_obtained = models.FloatField()
# # # #     total_marks = models.FloatField()
# # # #     date_recorded = models.DateField(auto_now_add=True)

# # # #     def __str__(self):
# # # #         return f"{self.student.user.username} - {self.course.title}"

# # # # class Transcript(models.Model):
# # # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # # #     gpa = models.FloatField()
# # # #     created_at = models.DateField(auto_now_add=True)

# # # #     def __str__(self):
# # # #         return f"{self.student.user.username} Transcript"

# # # # class GPA(models.Model):
# # # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # # #     semester = models.IntegerField()
# # # #     gpa_value = models.FloatField()

# # # #     def __str__(self):
# # # #         return f"{self.student.user.username} - Semester {self.semester}"


# # # # apps/results/models.py
# # # # Developed by SAYAB

# # # from django.db import models
# # # from apps.users.models import Student

# # # class Result(models.Model):
# # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # #     exam_name = models.CharField(max_length=200)
# # #     score = models.DecimalField(max_digits=5, decimal_places=2)
# # #     date = models.DateField(auto_now_add=True)

# # #     def __str__(self):
# # #         return f"{self.student.user.username} - {self.exam_name}"

# # # class Transcript(models.Model):
# # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # #     gpa = models.DecimalField(max_digits=4, decimal_places=2)
# # #     issued_date = models.DateField(auto_now_add=True)

# # #     def __str__(self):
# # #         return f"{self.student.user.username} - GPA: {self.gpa}"

# # # class GPA(models.Model):
# # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # #     semester = models.PositiveIntegerField()
# # #     gpa = models.DecimalField(max_digits=4, decimal_places=2)

# # #     def __str__(self):
# # #         return f"{self.student.user.username} - Sem {self.semester} - GPA {self.gpa}"

# # # apps/results/models.py
# # # Developed by SAYAB

# # from django.db import models
# # from apps.users.models import Student
# # from apps.courses.models import Course

# # class Result(models.Model):
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# #     marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)

# #     def __str__(self):
# #         return f"{self.student.user.username} - {self.course.name} - {self.marks_obtained}"

# # class Transcript(models.Model):
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"{self.student.user.username} - {self.created_at}"

# # File: backend/apps/results/models.py
# # Models for storing computed results (Developed by SAYAB)

# from django.db import models
# from django.conf import settings
# from apps.courses.models import Course

# class Result(models.Model):
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="results")
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
#     total_marks = models.DecimalField(max_digits=6, decimal_places=2)
#     published = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
# 

# File: backend/apps/results/models.py
# Result and Transcript models (Developed by SAYAB)

from django.db import models
from django.conf import settings
from apps.courses.models import Course

class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=8, decimal_places=2)
    total_marks = models.DecimalField(max_digits=8, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.grade and self.total_marks > 0:
            percentage = (float(self.marks_obtained) / float(self.total_marks)) * 100
            if percentage >= 85: self.grade = 'A'
            elif percentage >= 70: self.grade = 'B'
            elif percentage >= 60: self.grade = 'C'
            elif percentage >= 50: self.grade = 'D'
            else: self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Result: {self.student} - {self.course}"

class Transcript(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transcripts")
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="transcripts/", blank=True, null=True)

    def __str__(self):
        return f"Transcript: {self.student} ({self.issued_at.date()})"
