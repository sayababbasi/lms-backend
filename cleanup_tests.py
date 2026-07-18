import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

EMAILS = [
    "sayababbasi806@gmail.com",
    "management.revoticai@gmail.com",
    "founder.revoticai@gmail.com"
]

print("Starting Cleanup of Test Accounts...")
deleted_count = 0

for email in EMAILS:
    users = User.objects.filter(email=email)
    if users.exists():
        for user in users:
            print(f"Found user: {user.username} ({user.email}). Deleting...")
            user.delete()
            deleted_count += 1
    else:
        print(f"User with email {email} does not exist. Skipping.")

print(f"Cleanup complete. Deleted {deleted_count} accounts.")
