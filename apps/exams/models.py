# # # # # apps/exams/models.py
# # # # # Developed by SAYAB

# # # # from django.db import models
# # # # from apps.courses.models import Course
# # # # from apps.users.models import Student, Teacher

# # # # class Exam(models.Model):
# # # #     title = models.CharField(max_length=255)
# # # #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# # # #     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
# # # #     date = models.DateTimeField()

# # # #     def __str__(self):
# # # #         return self.title

# # # # class Question(models.Model):
# # # #     exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
# # # #     text = models.TextField()
# # # #     marks = models.FloatField(default=1)

# # # #     def __str__(self):
# # # #         return f"{self.exam.title} - {self.text[:50]}"

# # # # class ExamResult(models.Model):
# # # #     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
# # # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # # #     marks_obtained = models.FloatField()
# # # #     total_marks = models.FloatField()

# # # #     def __str__(self):
# # # #         return f"{self.student.user.username} - {self.exam.title}"


# # # # apps/exams/models.py
# # # # Developed by SAYAB

# # # from django.db import models
# # # from apps.users.models import Student, Teacher
# # # from apps.courses.models import Course

# # # class Exam(models.Model):
# # #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# # #     title = models.CharField(max_length=200)
# # #     date = models.DateField()
# # #     duration_minutes = models.PositiveIntegerField()
# # #     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

# # #     def __str__(self):
# # #         return self.title

# # # class Question(models.Model):
# # #     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
# # #     text = models.TextField()
# # #     max_marks = models.DecimalField(max_digits=5, decimal_places=2)

# # #     def __str__(self):
# # #         return f"{self.exam.title} - Q{self.id}"

# # # class ExamResult(models.Model):
# # #     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
# # #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# # #     score = models.DecimalField(max_digits=5, decimal_places=2)

# # #     def __str__(self):
# # #         return f"{self.student.user.username} - {self.exam.title} - {self.score}"

# # # apps/exams/models.py
# # # Developed by SAYAB

# # from django.db import models
# # from apps.courses.models import Course

# # class Exam(models.Model):
# #     title = models.CharField(max_length=255)
# #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# #     exam_date = models.DateTimeField()

# #     def __str__(self):
# #         return self.title

# # class Question(models.Model):
# #     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
# #     text = models.TextField()
# #     question_type = models.CharField(max_length=50, choices=[("MCQ","MCQ"),("Essay","Essay")])

# #     def __str__(self):
# #         return self.text

# # File: backend/apps/exams/models.py
# # Simple exam architecture including MCQ question bank (Developed by SAYAB)

# from django.db import models
# from django.conf import settings
# from apps.courses.models import Course

# class Exam(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
#     title = models.CharField(max_length=255)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)

# class Question(models.Model):
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
#     text = models.TextField()
#     marks = models.IntegerField(default=1)

# class MCQOption(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
#     text = models.CharField(max_length=255)
#     is_correct = models.BooleanField(default=False)


# File: backend/apps/exams/models.py
# Exams, Questions, MCQ options (Developed by SAYAB)

from django.db import models
from django.conf import settings
from apps.courses.models import Course

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"

class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('TEXT', 'Short/Long Text'),
        ('FILE', 'File Upload')
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='MCQ')
    marks = models.IntegerField(default=1)

    def __str__(self):
        return f"Q:{self.id} ({self.exam.title})"

class MCQOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=512)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Opt:{self.id} ({'Correct' if self.is_correct else 'Wrong'})"

class AdmitCard(models.Model):
    STATUS_CHOICES = (
        ('ISSUED', 'Issued'),
        ('BLOCKED', 'Blocked'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admit_cards")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="admit_cards")
    generated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BLOCKED')
    unique_code = models.UUIDField(default=None, null=True, blank=True)

    class Meta:
        unique_together = ['student', 'exam']

    def __str__(self):
        return f"AdmitCard: {self.student} - {self.exam} ({self.status})"

class ExamAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exam_attempts")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="attempts")
    start_time = models.DateTimeField(auto_now_add=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"Attempt: {self.student} - {self.exam}"

class ExamAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    selected_option = models.ForeignKey(MCQOption, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(blank=True, null=True)
    file_answer = models.FileField(upload_to='exams/answers/files/', blank=True, null=True)
    marks_awarded = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Answer: {self.attempt.student} - {self.question}"
