import os
import django
import sys

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from django.contrib.auth import get_user_model


User = get_user_model()

username = 'admin'
password = 'R@v0LMS@123'
email = 'admin@revotic.com'

try:
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. Updating password and permissions...")
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"User '{username}' updated successfully.")
    else:
        print(f"Creating user '{username}'...")
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"User '{username}' created successfully.")

except Exception as e:
    print(f"Error creating user: {e}")
    sys.exit(1)
