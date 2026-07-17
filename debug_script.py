from django.contrib.auth import get_user_model
from apps.users.models import Teacher
User = get_user_model()

print("--- DEBUG START ---")
print("Valid Teachers (is_teacher=True):", [u.username for u in User.objects.filter(is_teacher=True)])
print("All Teachers Profiles:", [(t.user.username, t.user.is_teacher) for t in Teacher.objects.all()])
print("--- DEBUG END ---")
