import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Teacher

User = get_user_model()

print("--- User Permissions Debug ---")
users = User.objects.all()
for u in users:
    print(f"User: {u.username} (ID: {u.id}) | Staff: {u.is_staff} | Super: {u.is_superuser} | Teacher: {u.is_teacher} | Student: {u.is_student}")

print("\n--- Teachers Debug ---")
teachers = Teacher.objects.all()
for t in teachers:
    print(f"Teacher Profile ID: {t.id} | User ID: {t.user.id} | User: {t.user.username} | is_teacher Flag: {t.user.is_teacher}")

print("\n--- Check Teacher Queryset for Serializer ---")
valid_teachers = User.objects.filter(is_teacher=True)
print(f"Users visible to CourseSerializer (is_teacher=True): {[u.username for u in valid_teachers]}")
