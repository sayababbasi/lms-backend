import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_crm.settings")
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

print("Sending synchronous Test Email...")
try:
    msg = EmailMultiAlternatives(
        subject="Sync Test",
        body="This is a synchronous test email to verify credentials.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["contact.revoticai@gmail.com"]
    )
    msg.send()
    print("Email sent successfully!")
except Exception as e:
    print(f"FAILED to send email: {e}")
