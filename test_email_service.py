import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from utils.email_service import EmailService
from django.contrib.auth import get_user_model
User = get_user_model()

def test_emails():
    # Let's get any admin user to test with, or fallback to the email in settings
    admin_user = User.objects.filter(is_superuser=True).first()
    
    test_email = admin_user.email if admin_user and admin_user.email else "test@example.com"
    print(f"Testing emails with {test_email}...")

    # For testing without Celery queue, we'll temporarily import the task function and call it directly.
    # Celery's .delay() is intercepted if CELERY_TASK_ALWAYS_EAGER is True, but we can just use send_template_email
    
    # Test 1: Welcome Email
    print("Sending Welcome Email...")
    success = EmailService.send_template_email(
        subject="Welcome to Revotic AI LMS!",
        recipient_list=[test_email],
        template_name="emails/notification.html",
        context={
            'heading': 'Welcome to Revotic AI LMS!',
            'message': f'Hello {admin_user.username if admin_user else "User"}, your account has been successfully created.<br><br><strong>Your Temporary Password:</strong> <code>12345678</code><br>Please log in and change your password immediately.',
        },
        log_email=True
    )
    print(f"Welcome Email Status: {'SUCCESS' if success else 'FAILED'}")

    # Print logs
    from apps.notifications.models import EmailLog
    logs = EmailLog.objects.all()[:5]
    print("\nRecent Email Logs:")
    for log in logs:
        print(f"- {log.subject} | Status: {log.status} | Sent At: {log.sent_at}")

if __name__ == "__main__":
    test_emails()
