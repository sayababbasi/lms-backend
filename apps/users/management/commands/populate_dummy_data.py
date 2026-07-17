import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.users.models import Student, Teacher, Staff
from apps.courses.models import Course, Module, Lesson, Resource, EnrollmentRequest
from apps.assignments.models import Assignment, Submission, Grade
from apps.exams.models import Exam, Question, MCQOption, AdmitCard
from apps.attendance.models import AttendanceRecord
from apps.finance.models import FeeChallan, Payment
from apps.library.models import Book
from apps.results.models import Result, Transcript
from apps.timetable.models import TimeSlot
from apps.notifications.models import Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data generation...'))
        
        # 1. Users
        self.create_users()
        
        # 2. Courses & Content
        self.create_courses()
        
        # 3. Enrollments (needed for other interactions)
        self.enroll_students()

        # 4. Assignments
        self.create_assignments()
        
        # 5. Exams
        self.create_exams()
        
        # 6. Attendance
        self.create_attendance()
        
        # 7. Finance
        self.create_finance()
        
        # 8. Library
        self.create_library()
        
        # 9. Results
        self.create_results()
        
        # 10. Timetable
        self.create_timetable()
        
        # 11. Notifications
        self.create_notifications()

        self.stdout.write(self.style.SUCCESS('Dummy data generation completed successfully!'))

    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Teachers
        for i in range(1, 6):
            username = f'teacher{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    is_teacher=True
                )
                Teacher.objects.create(
                    user=user,
                    department=random.choice(['CS', 'BBA', 'Engineering']),
                    designation='Lecturer',
                    qualification='PhD',
                    specialization='General'
                )
        
        # Students
        for i in range(1, 21):
            username = f'student{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    is_student=True
                )
                Student.objects.create(
                    user=user,
                    roll_number=f'ROLL-{1000+i}',
                    department=random.choice(['CS', 'BBA']),
                    program='BS',
                    semester=str(random.randint(1, 8)),
                    section=random.choice(['A', 'B'])
                )

        # Staff
        for i in range(1, 4):
            username = f'staff{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    is_staff=False # Django staff status
                )
                # Assuming simple Staff model usage
                Staff.objects.create(
                    user=user,
                    role='Admin Assistant',
                    designation='Junior Clerk'
                )

    def create_courses(self):
        self.stdout.write('Creating courses...')
        teachers = Teacher.objects.all()
        if not teachers.exists(): return

        titles = ['Intro to CS', 'Data Structures', 'Algorithms', 'Web Dev', 'Database Systems']
        
        for i, title in enumerate(titles):
            code = f'CS-{101+i}'
            teacher = random.choice(teachers)
            course, created = Course.objects.get_or_create(
                code=code,
                defaults={
                    'title': title,
                    'teacher': teacher.user,
                    'description': f'Description for {title}'
                }
            )
            
            # Modules
            for m in range(1, 4):
                module, _ = Module.objects.get_or_create(
                    course=course,
                    title=f'Module {m}: Topic {m}',
                    order=m
                )
                
                # Lessons
                for l in range(1, 3):
                    Lesson.objects.get_or_create(
                        module=module,
                        title=f'Lesson {l}',
                        defaults={
                            'content': 'This is dummy content.',
                            'order': l
                        }
                    )

    def enroll_students(self):
        self.stdout.write('Enrolling students...')
        students = Student.objects.all()
        courses = Course.objects.all()
        
        for student in students:
            # Enroll in 3 random courses
            enrolled_courses = random.sample(list(courses), min(len(courses), 3))
            for course in enrolled_courses:
                course.students.add(student)
                EnrollmentRequest.objects.get_or_create(
                    student=student.user,
                    course=course,
                    defaults={'status': 'APPROVED'}
                )

    def create_assignments(self):
        self.stdout.write('Creating assignments...')
        courses = Course.objects.all()
        for course in courses:
            for i in range(1, 3):
                Assignment.objects.get_or_create(
                    course=course,
                    title=f'Assignment {i}',
                    defaults={
                        'teacher': course.teacher,
                        'description': 'Dummy assignment description',
                        'due_date': timezone.now() + timedelta(days=7)
                    }
                )

    def create_exams(self):
        self.stdout.write('Creating exams...')
        courses = Course.objects.all()
        for course in courses:
            exam, created = Exam.objects.get_or_create(
                course=course,
                title=f'Midterm {course.code}',
                defaults={
                    'start_time': timezone.now() + timedelta(days=14),
                    'end_time': timezone.now() + timedelta(days=14, hours=2)
                }
            )
            
            if created:
                for q in range(1, 6):
                    question = Question.objects.create(
                        exam=exam,
                        text=f'Question {q} text?',
                        marks=5
                    )
                    MCQOption.objects.create(question=question, text='Option A', is_correct=True)
                    MCQOption.objects.create(question=question, text='Option B', is_correct=False)

    def create_attendance(self):
        self.stdout.write('Creating attendance...')
        courses = Course.objects.all()
        for course in courses:
            enrolled_students = course.students.all()
            for student in enrolled_students:
                for d in range(1, 6):
                    AttendanceRecord.objects.get_or_create(
                        student=student.user,
                        course=course,
                        date=timezone.now().date() - timedelta(days=d),
                        defaults={'present': random.choice([True, False])}
                    )

    def create_finance(self):
        self.stdout.write('Creating finance records...')
        students = Student.objects.all()
        for student in students:
            challan, created = FeeChallan.objects.get_or_create(
                student=student.user,
                amount=50000.00,
                due_date=timezone.now().date() + timedelta(days=30),
                defaults={'paid': random.choice([True, False])}
            )
            if challan.paid and created:
                Payment.objects.create(
                    challan=challan,
                    transaction_id=f'TXN-{random.randint(10000,99999)}',
                    amount=50000.00
                )

    def create_library(self):
        self.stdout.write('Creating library books...')
        for i in range(1, 11):
            Book.objects.get_or_create(
                title=f'Book Title {i}',
                author=f'Author {i}',
                isbn=f'ISBN-{1000+i}'
            )

    def create_results(self):
        self.stdout.write('Creating results...')
        courses = Course.objects.all()
        for course in courses:
            for student in course.students.all():
                if random.choice([True, False]):
                    Result.objects.get_or_create(
                        student=student.user,
                        course=course,
                        defaults={
                            'marks_obtained': random.uniform(50, 100),
                            'total_marks': 100.00,
                            'published': True
                        }
                    )

    def create_timetable(self):
        self.stdout.write('Creating timetable...')
        courses = Course.objects.all()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for course in courses:
            TimeSlot.objects.get_or_create(
                course=course,
                day=random.choice(days),
                start_time='09:00',
                end_time='10:30',
                defaults={'teacher': course.teacher, 'room_number': 'Room 101'}
            )

    def create_notifications(self):
        self.stdout.write('Creating notifications...')
        students = Student.objects.all()
        for student in students:
            Notification.objects.create(
                recipient=student.user,
                title='Welcome',
                message='Welcome to the University LMS!',
                read=False
            )
