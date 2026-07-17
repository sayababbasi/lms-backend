# # # # backend/apps/notifications/models.py
# # # # Developed by SAYAB

# # # from django.db import models
# # # from django.conf import settings

# # # class Notification(models.Model):
# # #     """
# # #     Model representing a notification for a student or staff member.
# # #     """

# # #     NOTIFICATION_TYPES = [
# # #         ('info', 'Info'),
# # #         ('warning', 'Warning'),
# # #         ('alert', 'Alert'),
# # #         ('success', 'Success'),
# # #     ]

# # #     title = models.CharField(max_length=200, help_text="Title of the notification")
# # #     message = models.TextField(help_text="Detailed message content")
# # #     recipient = models.ForeignKey(
# # #         settings.AUTH_USER_MODEL,
# # #         on_delete=models.CASCADE,
# # #         related_name='notifications',
# # #         help_text="The user who will receive this notification"
# # #     )
# # #     notification_type = models.CharField(
# # #         max_length=20,
# # #         choices=NOTIFICATION_TYPES,
# # #         default='info',
# # #         help_text="Type/category of the notification"
# # #     )
# # #     is_read = models.BooleanField(default=False, help_text="Has the notification been read?")
# # #     created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when notification was created")
# # #     updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when notification was last updated")

# # #     class Meta:
# # #         verbose_name = "Notification"
# # #         verbose_name_plural = "Notifications"
# # #         ordering = ['-created_at']

# # #     def __str__(self):
# # #         return f"{self.title} → {self.recipient.username}"


# # # apps/notifications/models.py
# # # Developed by SAYAB

# # from django.db import models
# # from apps.users.models import Student, Teacher

# # class Notification(models.Model):
# #     recipient_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
# #     recipient_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
# #     message = models.TextField()
# #     notification_type = models.CharField(max_length=50, choices=[("Info","Info"),("Alert","Alert")])
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"{self.message[:50]} - {self.created_at}"

# # File: backend/apps/notifications/models.py
# # Simple notification log model (Developed by SAYAB)

# from django.db import models
# from django.conf import settings

# class Notification(models.Model):
#     recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
#     title = models.CharField(max_length=255)
#     message = models.TextField()
#     read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

# File: backend/apps/notifications/models.py
# Notification log model (Developed by SAYAB)

from django.db import models
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification: {self.title} -> {self.recipient}"

class Message(models.Model):
    """
    Model representing a direct message between users.
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"From {self.sender} to {self.recipient} at {self.created_at}"
