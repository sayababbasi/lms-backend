from django.db import models
from django.conf import settings
from apps.courses.models import Course

class Assignment(models.Model):
    ASSIGNMENT_TYPES = [
        ('Homework', 'Homework'), ('Project', 'Project'), ('Lab', 'Lab'),
        ('Quiz', 'Quiz Assignment'), ('Presentation', 'Presentation'),
        ('Case Study', 'Case Study'), ('Essay', 'Essay'),
        ('Programming', 'Programming Assignment'), ('Research Paper', 'Research Paper'),
        ('Group', 'Group Assignment'), ('Practical', 'Practical Assignment'),
        ('Reading', 'Reading Assignment'), ('Custom', 'Custom Type')
    ]
    
    SUBMISSION_TYPES = [
        ('Online Text', 'Online Text'), ('File Upload', 'File Upload'),
        ('External URL', 'External URL'), ('Mixed', 'Mixed Submission'),
        ('None', 'No Submission Needed')
    ]

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Scheduled', 'Scheduled'),
        ('Published', 'Published'),
        ('Closed', 'Closed'),
        ('Archived', 'Archived')
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_assignments', null=True, blank=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) # Rich Text
    instructions = models.TextField(blank=True, null=True)
    
    # Grading Settings
    max_score = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    weightage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    assignment_type = models.CharField(max_length=50, choices=ASSIGNMENT_TYPES, default='Homework')
    
    # Time Settings
    publish_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=100, default='UTC')
    
    # Submission Settings
    submission_type = models.CharField(max_length=50, choices=SUBMISSION_TYPES, default='File Upload')
    allow_resubmission = models.BooleanField(default=False)
    max_attempts = models.IntegerField(default=1)
    
    # Late Policy
    allow_late = models.BooleanField(default=False)
    late_days_allowed = models.IntegerField(default=0)
    late_penalty_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Advanced
    is_group_assignment = models.BooleanField(default=False)
    anonymous_grading = models.BooleanField(default=False)
    peer_review = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        course_code = self.course.code if self.course else 'No Course'
        return f"{course_code} - {self.title}"


class AssignmentAttachment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='assignments/attachments/')
    filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename or f"Attachment for {self.assignment.title}"


class Rubric(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rubrics')
    assignment = models.OneToOneField(Assignment, on_delete=models.SET_NULL, null=True, blank=True, related_name='rubric')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RubricCriteria(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, related_name='criteria')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    max_points = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)

    def __str__(self):
        return f"{self.rubric.title} - {self.title}"


class Submission(models.Model):
    """
    Student submission attempt.
    """
    SUBMISSION_STATUS = [
        ('Draft', 'Draft'),
        ('Submitted', 'Submitted'),
        ('Returned', 'Returned'),
        ('Graded', 'Graded')
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    
    status = models.CharField(max_length=20, choices=SUBMISSION_STATUS, default='Draft')
    attempt_number = models.IntegerField(default=1)
    
    is_late = models.BooleanField(default=False)
    
    # Content
    text_content = models.TextField(blank=True, null=True, help_text="Online text submission")
    external_url = models.URLField(blank=True, null=True)
    
    # Plagiarism (Ready for future integration)
    plagiarism_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['assignment', 'student', 'attempt_number']

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title} (Attempt {self.attempt_number})"


class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='submissions/files/')
    filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename or f"File for {self.submission}"


class SubmissionComment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Grade(models.Model):
    """
    Grade and feedback for a submission.
    """
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='graded_assignments')
    
    score = models.DecimalField(max_digits=6, decimal_places=2, help_text="Final Score")
    rubric_score_data = models.JSONField(blank=True, null=True, help_text="Stored breakdown of rubric points")
    
    feedback = models.TextField(blank=True, null=True)
    private_notes = models.TextField(blank=True, null=True, help_text="Notes only visible to teachers")
    
    is_published = models.BooleanField(default=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.submission} - {self.score}"

class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    target_type = models.CharField(max_length=50) # Assignment, Submission, Grade
    target_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
