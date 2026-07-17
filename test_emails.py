import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_crm.settings")
django.setup()

from utils.email_service import EmailService

class MockUser:
    def __init__(self, email, username):
        self.email = email
        self.username = username

# The provided email
user = MockUser("contact.revoticai@gmail.com", "Admin")

print("Sending Test Email...")
EmailService.send_welcome_email(user, "testpassword123")
print("Email queued!")
