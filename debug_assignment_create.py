from django.contrib.auth import get_user_model
from apps.assignments.models import Assignment
from apps.courses.models import Course
from apps.assignments.serializers import AssignmentSerializer
from rest_framework.test import APIRequestFactory

User = get_user_model()

print("--- DEBUG ASSIGNMENT CREATE ---")

# Get a user and course
user = User.objects.filter(is_superuser=True).first()
course = Course.objects.first()

if not user or not course:
    print("Missing user or course")
    exit()

print(f"User: {user.username}, Course: {course.title} ({course.id})")

data = {
    "title": "Debug Assignment",
    "description": "Test description",
    "due_date": "2025-12-30T12:00:00",
    "course": course.id
}

print(f"Data Payload: {data}")

# Simulate Serializer Validation
serializer = AssignmentSerializer(data=data)
if serializer.is_valid():
    print("Serializer Valid!")
    # Simulate ViewSet perform_create logic
    try:
        serializer.save(teacher=user)
        print("Save Successful!")
        print("Created:", serializer.data)
    except Exception as e:
        print("Save Failed:", e)
else:
    print("Serializer Errors:", serializer.errors)
