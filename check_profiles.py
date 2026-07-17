import os
import django
import sys

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Student

User = get_user_model()

def check_profiles():
    print("Checking student profiles...")
    students = User.objects.filter(username__startswith='student')
    
    for u in students:
        has_profile = hasattr(u, 'student_profile')
        print(f"User: {u.username} (ID: {u.id}) - Has Profile: {has_profile}")
        if has_profile:
             print(f"   -> Profile ID: {u.student_profile.id}")
        else:
             print(f"   -> [WARNING] No Student Profile!")

if __name__ == '__main__':
    check_profiles()
