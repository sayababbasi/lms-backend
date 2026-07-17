import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from apps.users.serializers import StudentSerializer
from apps.users.models import User

def debug_create_student():
    print("DEBUG: Starting Student Creation Test")
    data = {
        "user": {
            "username": "debug_student_01",
            "email": "debug01@example.com",
            "first_name": "Debug",
            "last_name": "User",
            "phone": "9999999999",
            "address": "Debug Address",
            "gender": "M",
            "date_of_birth": "2000-01-01",
            "cnic": "99999-9999999-9"
        },
        "roll_number": "DBG-001",
        "department": "Debug Dept",
        "program": "BSCS",
        "semester": "1",
        "section": "A",
        "admission_date": "2024-01-01",
        "guardian_name": "Debug Guardian",
        "guardian_contact": "5555555555"
    }

    # Clean previous
    User.objects.filter(username="debug_student_01").delete()

    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        try:
            print("Serializer is valid. Attempting save...")
            serializer.save()
            print("SUCCESS: Student saved.")
        except Exception:
            traceback.print_exc()
    else:
        print("VALIDATION ERROR:", serializer.errors)

if __name__ == "__main__":
    debug_create_student()
