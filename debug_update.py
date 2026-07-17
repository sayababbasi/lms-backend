import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from apps.users.serializers import StudentSerializer
from apps.users.models import Student, User

def debug_update_student():
    print("DEBUG: Starting Student Update Test")
    
    # 1. Create a student
    user_data = {
        "username": "update_test_user",
        "email": "updatetest@example.com",
        "first_name": "Before",
        "last_name": "Update"
    }
    
    # Clean previous
    User.objects.filter(username="update_test_user").delete()
    
    user = User.objects.create_user(**user_data, password="password123")
    user.is_student = True
    user.save()
    
    student = Student.objects.create(
        user=user,
        roll_number="UPD-001",
        department="CS",
        admission_date="2024-01-01"
    )
    
    print(f"Created student {student.id} with user {user.id}")

    # 2. Try to update it (Simulating the payload that causes 400)
    # The frontend typically sends the SAME username/email back.
    update_data = {
        "user": {
            "username": "update_test_user",  # Same username
            "email": "updatetest@example.com", # Same email
            "first_name": "After",
            "last_name": "Update"
        },
        "roll_number": "UPD-001",
        "department": "CS Updated"
    }

    print("\nAttempting Update...")
    serializer = StudentSerializer(instance=student, data=update_data, partial=True)
    
    if serializer.is_valid():
        try:
            serializer.save()
            print("SUCCESS: Student updated.")
            print("New Name:", student.user.first_name)
        except Exception:
            traceback.print_exc()
    else:
        print("VALIDATION ERROR:", serializer.errors)

if __name__ == "__main__":
    debug_update_student()
