import os
import django
import sys

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from apps.courses.models import EnrollmentRequest
from rest_framework.test import APIRequestFactory
from apps.courses.views import EnrollmentRequestViewSet

def debug_enrollments():
    print("Checking Enrollment Requests...")
    reqs = EnrollmentRequest.objects.filter(status='PENDING')
    print(f"Found {reqs.count()} PENDING requests.")
    
    for req in reqs:
        print(f"Request ID: {req.id} - Student: {req.student.username} (ID: {req.student.id})")
        
        # Test Approval Logic manualy
        try:
            if hasattr(req.student, 'student_profile'):
                print(f"   -> User has profile. Logic should work.")
                # We won't save, just check logic
                # req.course.students.add(req.student.student_profile)
            else:
                print(f"   -> [ERROR] User has NO profile!")
        except Exception as e:
            print(f"   -> Exception: {e}")

if __name__ == '__main__':
    debug_enrollments()
