import os
import django
from django.contrib.auth import get_user_model

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

User = get_user_model()
USERNAME = 'sayab'
PASSWORD = 'R@v0LMS@123'
EMAIL = 'sayab@example.com'  # Using a placeholder email

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print(f"Superuser '{USERNAME}' created.")
else:
    print(f"Superuser '{USERNAME}' already exists. resetting password.")
    u = User.objects.get(username=USERNAME)
    u.set_password(PASSWORD)
    u.save()
    print(f"Password for '{USERNAME}' has been updated.")
