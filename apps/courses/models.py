from django.db import models
from django.conf import settings
from utils.storages import CourseThumbnailStorage, DocumentStorage, SubmissionStorage

class Course(models.Model):
    """
    Course model representing a subject or class.
    """
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='courses', null=True, blank=True)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teaching_courses', blank=True)
    students = models.ManyToManyField('users.Student', related_name='courses', blank=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', storage=CourseThumbnailStorage, blank=True, null=True)
    
    # Advanced LMS Fields
    credit_hours = models.PositiveIntegerField(default=3)
    passing_percentage = models.PositiveIntegerField(default=50)
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    semester = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Fall 2026")
    category = models.CharField(max_length=100, blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

class Module(models.Model):
    """
    Module/Section within a course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.code} - {self.title}"

class Lesson(models.Model):
    """
    Lesson within a module (e.g., a specific lecture topic).
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, help_text="Text content or markdown")
    video_url = models.URLField(blank=True, null=True, help_text="Link to video lecture")
    order = models.PositiveIntegerField(default=1)

    # YouTube Upload Fields
    youtube_video_id = models.CharField(max_length=100, blank=True, null=True)
    youtube_embed_url = models.URLField(blank=True, null=True)
    video_duration = models.CharField(max_length=50, blank=True, null=True)
    upload_status = models.CharField(max_length=50, default='pending')
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"

class Resource(models.Model):
    """
    Downloadable resources or extra links for a lesson.
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255, default="Resource")
    file = models.FileField(upload_to='lesson_resources/', storage=DocumentStorage, blank=True, null=True)
    external_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class EnrollmentRequest(models.Model):
    """
    Request from a student to enroll in a course.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollment_requests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_requests')
    payment_proof = models.ImageField(upload_to='payment_proofs/', storage=SubmissionStorage, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} -> {self.course} ({self.status})"

