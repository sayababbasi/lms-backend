from django.contrib.auth import get_user_model
from apps.users.models import Teacher
User = get_user_model()

print("--- FIX START ---")
teachers = Teacher.objects.all()
for t in teachers:
    if not t.user.is_teacher:
        print(f"Fixing user {t.user.username}... setting is_teacher=True")
        t.user.is_teacher = True
        t.user.save()
    else:
        print(f"User {t.user.username} is already good.")

print("--- FIX END ---")
