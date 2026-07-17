import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from apps.assignments.models import Assignment
from apps.courses.models import Course
from apps.users.models import User

def create_dummy_assignments():
    print("Creating dummy assignments...")
    
    # Get all courses
    courses = Course.objects.all()
    if not courses.exists():
        print("No courses found. Please create courses first.")
        return
    
    # Get a teacher user
    teacher = User.objects.filter(is_teacher=True).first()
    if not teacher:
        print("No teacher found. Creating a teacher user...")
        teacher = User.objects.filter(is_staff=True).first()
        if not teacher:
            print("Error: No teacher or admin user found.")
            return
    
    # Create assignments for each course
    for course in courses:
        # Check if assignments already exist for this course
        existing = Assignment.objects.filter(course=course).count()
        if existing > 0:
            print(f"Course '{course.title}' already has {existing} assignment(s)")
            continue
        
        # Create 2-3 assignments per course
        assignments_data = [
            {
                'title': f'{course.code} - Assignment 1: Fundamentals',
                'description': f'Complete the fundamental concepts assignment for {course.title}. This assignment covers the basic principles and foundational knowledge required for this course.',
                'due_date': datetime.now() + timedelta(days=7)
            },
            {
                'title': f'{course.code} - Assignment 2: Practical Application',
                'description': f'Apply the concepts learned in {course.title} to solve real-world problems. Submit your solutions with detailed explanations and code if applicable.',
                'due_date': datetime.now() + timedelta(days=14)
            },
            {
                'title': f'{course.code} - Mid-Term Project',
                'description': f'Mid-term project for {course.title}. This is a comprehensive assignment that tests your understanding of all topics covered so far. Work individually and submit before the deadline.',
                'due_date': datetime.now() + timedelta(days=21)
            }
        ]
        
        for data in assignments_data:
            assignment = Assignment.objects.create(
                course=course,
                teacher=teacher,
                **data
            )
            print(f"Created: {assignment.title}")
    
    total_assignments = Assignment.objects.count()
    print(f"\nTotal assignments in database: {total_assignments}")
    
    # Display assignments by course
    print("\nAssignments by Course:")
    for course in courses:
        course_assignments = Assignment.objects.filter(course=course)
        print(f"\n{course.code} - {course.title}:")
        for assignment in course_assignments:
            print(f"  * {assignment.title} (Due: {assignment.due_date.strftime('%Y-%m-%d')})")

if __name__ == '__main__':
    create_dummy_assignments()
    print("\nDone! Refresh your browser to see the assignments.")
