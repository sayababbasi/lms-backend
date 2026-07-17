import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from apps.users.models import User, Student
from apps.courses.models import Course
from apps.assignments.models import Assignment

def check_and_enroll_students():
    print("Checking student enrollment status...\n")
    
    # Get all students
    students = Student.objects.all()
    if not students.exists():
        print("ERROR: No students found in database!")
        return
    
    # Get all courses
    courses = Course.objects.all()
    if not courses.exists():
        print("ERROR: No courses found in database!")
        return
    
    print(f"Found {students.count()} students and {courses.count()} courses\n")
    
    # Check each student's enrollment
    for student in students:
        user = student.user
        enrolled = student.courses.all()
        enrolled_count = enrolled.count()
        
        print(f"Student: {user.username} ({user.first_name} {user.last_name})")
        print(f"  Currently enrolled in: {enrolled_count} courses")
        
        if enrolled_count == 0:
            print(f"  Enrolling {user.username} in all courses...")
            for course in courses:
                student.courses.add(course)
            print(f"  Enrolled in {courses.count()} courses")
        else:
            print(f"  Courses: {', '.join([c.code for c in enrolled])}")
        
        # Show assignments for this student
        enrolled_course_ids = student.courses.values_list('id', flat=True)
        assignments = Assignment.objects.filter(course_id__in=enrolled_course_ids)
        print(f"  Available assignments: {assignments.count()}\n")

if __name__ == '__main__':
    check_and_enroll_students()
    print("\nDone! Student enrollment verified.")
