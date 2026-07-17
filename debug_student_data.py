import os
import django
import sys

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.courses.models import Course
from apps.users.models import Student

User = get_user_model()

def debug_data():
    username = 'student1'
    try:
        user = User.objects.get(username=username)
        # Fix name
        if not user.first_name:
             user.first_name = 'Alice'
             user.save()
             print("Updated student1 first_name to Alice")
        
        print(f"User found: {user.username} (ID: {user.id})")
        
        if hasattr(user, 'student_profile'):
            student = user.student_profile
            print(f"Student Profile found: ID {student.id}")
            
            # Check Enrollments
            courses = Course.objects.filter(students=student)
            print(f"Enrolled Courses Count: {courses.count()}")
            for c in courses:
                print(f" - {c.code}: {c.title}")
                
            # Check logic used in View
            from apps.assignments.models import Assignment, Submission
            
            enrolled_course_ids = courses.values_list('id', flat=True)
            total_assignments = Assignment.objects.filter(course_id__in=enrolled_course_ids).count()
            print(f"Total Assignments in these courses: {total_assignments}")
            
        else:
            print("NO Student Profile found for this user.")
            
    except User.DoesNotExist:
        print(f"User {username} NOT found.")

if __name__ == '__main__':
    debug_data()
