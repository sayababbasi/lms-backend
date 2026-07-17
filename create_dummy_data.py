import os
import django
import sys
from django.utils import timezone
from datetime import timedelta

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Student, Teacher
from apps.courses.models import Course, Module, Lesson
from apps.assignments.models import Assignment

User = get_user_model()

def create_dummy_data():
    print("Creating dummy data...")

    # 1. Create Teacher
    teacher_user, created = User.objects.get_or_create(username='teacher1', defaults={
        'email': 'teacher1@revotic.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'is_teacher': True
    })
    if created:
        teacher_user.set_password('password123')
        teacher_user.save()
        Teacher.objects.create(user=teacher_user, department='Computer Science', designation='Lecturer')
        print("Teacher 'teacher1' created.")
    else:
        print("Teacher 'teacher1' already exists.")

    # 2. Create Student
    student_user, created = User.objects.get_or_create(username='student1', defaults={
        'email': 'student1@revotic.com',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'is_student': True
    })
    if created:
        student_user.set_password('password123')
        student_user.save()
        Student.objects.create(
            user=student_user, 
            roll_number='CS-2024-001', 
            department='Computer Science',
            program='BSCS',
            semester='1st'
        )
        print("Student 'student1' created.")
    else:
        print("Student 'student1' already exists.")

    # 3. Create Course
    course, created = Course.objects.get_or_create(code='CS101', defaults={
        'title': 'Introduction to Computer Science',
        'description': 'Fundamental concepts of computing and programming.',
        'teacher': teacher_user
    })
    if created:
        print("Course 'CS101' created.")
    else:
        print("Course 'CS101' already exists.")

    # 4. Enroll Student
    student_profile = student_user.student_profile
    if not course.students.filter(id=student_profile.id).exists():
        course.students.add(student_profile)
        print(f"Student 'student1' enrolled in 'CS101'.")
    else:
        print(f"Student 'student1' already enrolled in 'CS101'.")

    # 5. Create Assignment
    assignment, created = Assignment.objects.get_or_create(
        title='Algorithm Basics', 
        course=course,
        defaults={
            'description': 'Write a flowchart for a simple algorithm.',
            'due_date': timezone.now() + timedelta(days=7)
        }
    )
    if created:
        print("Assignment 'Algorithm Basics' created.")
    else:
        print("Assignment 'Algorithm Basics' already exists.")

if __name__ == '__main__':
    create_dummy_data()
