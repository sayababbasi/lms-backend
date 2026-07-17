# File: backend/apps/users/signals.py
# Signals for creating profiles or onboarding tasks after user creation (Developed by SAYAB)

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        # Placeholder for post-registration tasks (send welcome email, create profile, etc.)
        if instance.is_student:
            # create student profile or add to default groups
            pass
        if instance.is_teacher:
            # create teacher-specific resources
            pass
