import os
import django
import sys
import json

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings") # Try 'core.settings' first, check manage.py if it fails
if 'lms_crm.settings' in open('manage.py').read():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lms_crm.settings'

django.setup()

from django.contrib.auth import get_user_model
from apps.assignments.models import Assignment
from apps.courses.models import Course
from apps.assignments.serializers import AssignmentSerializer

User = get_user_model()

print("\n--- STANDALONE DEBUG ASSIGNMENT CREATE ---")

user = User.objects.filter(is_superuser=True).first()
course = Course.objects.first()

if not user or not course:
    print("FATAL: Missing user or course")
    sys.exit(1)

print(f"User: {user.username} (ID: {user.id})")
print(f"Course: {course.title} (ID: {course.id})")

# Test Case 1: Ideal Payload
print("\n--- Test 1: Ideal Payload (Int ID) ---")
data_1 = {
    "title": "Debug Assignment Int",
    "description": "Test description",
    "due_date": "2025-12-30T12:00:00",
    "course": course.id
}
ser_1 = AssignmentSerializer(data=data_1)
if ser_1.is_valid():
    print("Valid!")
else:
    print("Invalid:", json.dumps(ser_1.errors, indent=2))

# Test Case 2: Frontend Payload (String ID, datetime-local format)
print("\n--- Test 2: Frontend Payload (String ID, No Seconds) ---")
data_2 = {
    "title": "Debug Assignment String",
    "description": "Test description",
    "due_date": "2025-12-30T12:00",  # Frontend sends this
    "course": str(course.id)        # Frontend sends string "1"
}
ser_2 = AssignmentSerializer(data=data_2)
if ser_2.is_valid():
    print("Valid!")
else:
    print("Invalid:", json.dumps(ser_2.errors, indent=2))
