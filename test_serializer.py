import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from apps.users.serializers import StudentSerializer
from apps.users.models import User, Student

def test_create_student():
    data = {
        "user": {
            "username": "serializer_test_user",
            "email": "serializer_test@example.com",
            "first_name": "Serializer",
            "last_name": "Test",
            "phone": "1234567890",
            "gender": "M",
            "date_of_birth": "2000-01-01",
            "cnic": "11111-1111111-1"
        },
        "roll_number": "TEST-2024-001",
        "department": "CS",
        "program": "BSCS",
        "semester": "1",
        "section": "A",
        "guardian_name": "Guardian",
        "guardian_contact": "0000000000"
    }

    # Clean up if exists
    User.objects.filter(username="serializer_test_user").delete()

    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        try:
            student = serializer.save()
            print("SUCCESS: Student created via serializer.")
            print(f"User ID: {student.user.id}, Username: {student.user.username}")
            print(f"Student Roll No: {student.roll_number}")
            print(f"Profile Picture: {student.user.profile_picture}")
            
            # Verify fields
            if student.program == 'BSCS' and student.user.cnic == '11111-1111111-1':
                print("Field verification: PASS")
            else:
                print("Field verification: FAIL")

        except Exception as e:
            print(f"FAILED to save: {e}")
    else:
        print("Serializer errors:", serializer.errors)

if __name__ == "__main__":
    test_create_student()
