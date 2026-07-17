from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user extending Django AbstractUser.
    Roles:
      - is_student
      - is_teacher
      - is_staff (Django built-in) for Admins
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    PASSWORD_STATUS_CHOICES = [
        ('TEMPORARY', 'Temporary'),
        ('PERMANENT', 'Permanent'),
        ('EXPIRED', 'Expired'),
        ('RESET_REQUIRED', 'Reset Required'),
        ('LOCKED', 'Locked'),
        ('INACTIVE', 'Inactive'),
        ('ACTIVE', 'Active'),
    ]

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_exam_officer = models.BooleanField(default=False)
    
    # Password Management Fields
    password_status = models.CharField(max_length=20, choices=PASSWORD_STATUS_CHOICES, default='TEMPORARY')
    force_password_change = models.BooleanField(default=True)
    last_password_change = models.DateTimeField(default=timezone.now)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)
    
    # Common Profile Fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    cnic = models.CharField(max_length=20, blank=True, null=True, verbose_name="CNIC")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    program = models.CharField(max_length=100, blank=True, null=True)  # e.g., BSCS, BBA
    semester = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    admission_date = models.DateField(default=timezone.now)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True) # e.g. Lecturer, Professor
    qualification = models.CharField(max_length=200, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    joining_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.CharField(max_length=100) # Designation e.g. Accountant, Admin
    designation = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username

class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')
    hashed_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Password History for {self.user.username} at {self.created_at}"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs_target')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs_actor')
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} by {self.admin} on {self.user} at {self.timestamp}"

class OrganizationSettings(models.Model):
    # In a multi-tenant system, this would link to an Organization model.
    # For now, acting as global settings.
    min_password_length = models.IntegerField(default=8)
    expiration_days = models.IntegerField(default=90)
    max_failed_attempts = models.IntegerField(default=5)
    require_special_chars = models.BooleanField(default=True)
    require_uppercase = models.BooleanField(default=True)
    require_numbers = models.BooleanField(default=True)

    def __str__(self):
        return "Global Organization Settings"
