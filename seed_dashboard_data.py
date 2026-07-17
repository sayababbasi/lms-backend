import os
import django
import sys
from django.utils import timezone
from datetime import timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Student, Teacher
from apps.courses.models import Course
from apps.assignments.models import Assignment, Submission
from apps.timetable.models import TimeSlot

User = get_user_model()

def run():
    try:
        teacher_user = User.objects.get(username='teacher1')
    except User.DoesNotExist:
        print("Teacher1 not found. Run create_dummy_data.py first.")
        return

    try:
        student_user = User.objects.get(username='student1')
    except User.DoesNotExist:
        print("Student1 not found. Run create_dummy_data.py first.")
        return
        
    print("Creating courses...")
    courses_data = [
        ('ENG201', 'Advanced English Literature'),
        ('MATH301', 'Calculus III'),
        ('PHY101', 'Physics for Engineers'),
        ('HIST105', 'World History'),
    ]
    
    course_objs = []
    for code, title in courses_data:
        c, _ = Course.objects.get_or_create(code=code, defaults={
            'title': title,
            'description': f'Detailed study of {title}',
            'teacher': teacher_user
        })
        c.students.add(student_user.student_profile)
        course_objs.append(c)

    print("Creating assignments...")
    for i, course in enumerate(course_objs):
        for j in range(2):
            Assignment.objects.get_or_create(
                title=f'Assignment {j+1} for {course.code}',
                course=course,
                defaults={
                    'description': 'Please complete the attached exercises.',
                    'due_date': timezone.now() + timedelta(days=j*3 + 1),
                    'max_score': 100,
                    'max_attempts': 3
                }
            )

    print("Creating submissions...")
    assignment_to_submit = Assignment.objects.filter(course__in=course_objs).first()
    if assignment_to_submit:
        Submission.objects.get_or_create(
            assignment=assignment_to_submit,
            student=student_user,
            defaults={
                'text_content': 'Here is my completed work for the assignment.',
                'status': 'SUBMITTED'
            }
        )

    print("Creating timetable...")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    # Adding today as well so it shows up in dashboard
    today_str = timezone.now().strftime('%A')
    if today_str not in days:
        days.append(today_str)

    for day in days:
        for i, course in enumerate(course_objs):
            try:
                TimeSlot.objects.get_or_create(
                    course=course,
                    teacher=teacher_user,
                    day=day,
                    start_time=time(hour=9 + i, minute=0),
                    defaults={
                        'end_time': time(hour=10 + i, minute=0),
                        'room_number': f'Room 10{i}'
                    }
                )
            except Exception as e:
                print(f"Error creating timeslot for {course.code}: {e}")

    print("Data seeded successfully.")

run()
