import os
import django
import sys
import traceback

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

User = get_user_model()

def debug_view():
    print("Debugging StudentStatsView Logic...")
    try:
        user = User.objects.get(username='student1')
        print(f"User: {user.username} (ID: {user.id})")
        
        if hasattr(user, 'student_profile'):
            student_profile = user.student_profile
            print(f"StudentProfile ID: {student_profile.id}")
        else:
            print("ERROR: User has no student_profile")
            return

        # Mimic View Logic
        from apps.courses.models import Course
        from apps.assignments.models import Assignment, Submission
        # CORRECTED MODEL IMPORT
        from apps.attendance.models import AttendanceRecord

        print("1. Checking Courses...")
        enrolled_courses = Course.objects.filter(students=student_profile)
        print(f"   Count: {enrolled_courses.count()}")
        
        print("2. Checking Assignments...")
        enrolled_course_ids = enrolled_courses.values_list('id', flat=True)
        total = Assignment.objects.filter(course_id__in=enrolled_course_ids).count()
        print(f"   Total Assignments: {total}")
        
        print("3. Checking Submissions (User based)...")
        subs = Submission.objects.filter(student=user, assignment__course_id__in=enrolled_course_ids).count()
        print(f"   Submissions: {subs}")
        
        print("4. Checking Attendance (User based)...")
        # CORRECTED QUERY
        att_count = AttendanceRecord.objects.filter(student=user).count()
        print(f"   Attendance Records: {att_count}")
        
        print("SUCCESS! No error found in logic flow.")
        
    except Exception as e:
        print("\n!!! ERROR DETECTED !!!")
        traceback.print_exc()

if __name__ == '__main__':
    debug_view()
