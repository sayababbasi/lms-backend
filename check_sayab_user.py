import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from apps.users.models import User, Student
from apps.courses.models import Course

def check_user_sayab():
    print("Checking user 'sayab'...\n")
    
    try:
        user = User.objects.get(username='sayab')
        print(f"User found: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Is Student: {user.is_student}")
        print(f"  Is Teacher: {user.is_teacher}")
        print(f"  Is Staff: {user.is_staff}")
        print(f"  Has student_profile: {hasattr(user, 'student_profile')}")
        
        if hasattr(user, 'student_profile'):
            student = user.student_profile
            courses = student.courses.all()
            print(f"\n  Student Profile ID: {student.id}")
            print(f"  Roll Number: {student.roll_number}")
            print(f"  Enrolled in {courses.count()} courses:")
            for course in courses:
                print(f"    - {course.code}: {course.title}")
        else:
            print("\n  WARNING: User does not have a student profile!")
            print("  Setting user as student and creating profile...")
            user.is_student = True
            user.save()
            
            student = Student.objects.create(
                user=user,
                roll_number=f"STD-{user.id:04d}",
                department="Computer Science",
                program="BSCS",
                semester="1"
            )
            print(f"  Created student profile with ID: {student.id}")
            
            # Enroll in some courses
            print("  Enrolling in all available courses...")
            courses = Course.objects.all()
            for course in courses:
                student.courses.add(course)
            print(f"  Enrolled in {courses.count()} courses")
            
    except User.DoesNotExist:
        print("ERROR: User 'sayab' not found!")
        print("\nAvailable users:")
        for u in User.objects.all()[:10]:
            print(f"  - {u.username} (is_student: {u.is_student}, is_teacher: {u.is_teacher})")

if __name__ == '__main__':
    check_user_sayab()
    print("\nDone!")
