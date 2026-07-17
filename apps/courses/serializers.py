from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Module, Lesson, Resource, EnrollmentRequest
from apps.users.serializers import StudentSerializer

class ResourceSerializer(serializers.ModelSerializer):
    lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        source='lesson',
        write_only=True,
        required=False
    )
    class Meta:
        model = Resource
        fields = ['id', 'title', 'file', 'external_url', 'lesson_id']

class LessonSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)
    module_id = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        source='module',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order', 'resources', 'module_id', 'youtube_video_id', 'youtube_embed_url', 'upload_status', 'video_duration']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons', 'course_id']

class CourseSerializer(serializers.ModelSerializer):
    # Teacher is read-only for display, but we allow writing via teacher_id
    teacher = serializers.StringRelatedField(read_only=True)
    teachers = serializers.StringRelatedField(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    
    # Legacy write support
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_teacher=True),
        source='teacher',
        write_only=True,
        required=False
    )
    
    # New M2M write support
    teacher_ids = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_teacher=True),
        source='teachers',
        many=True,
        required=False
    )
    
    # Students enrollment
    student_ids = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_student=True),
        source='students',
        write_only=True,
        many=True,
        required=False
    )
    
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'description', 'thumbnail', 'teacher', 'teachers', 'teacher_id', 'teacher_ids', 'students', 'student_ids', 'created_at', 'modules']

class CourseDetailSerializer(CourseSerializer):
    """
    Detailed view with full module/lesson structure.
    """
    pass

class CourseListSerializer(serializers.ModelSerializer):
    """
    Lighter view for lists (no modules).
    """
    teacher = serializers.StringRelatedField(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(source='teacher', read_only=True)
    teacher_ids = serializers.PrimaryKeyRelatedField(source='teachers', many=True, read_only=True)
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'teacher', 'teacher_id', 'teacher_ids', 'created_at', 'thumbnail', 'description', 'students_count']

    def get_students_count(self, obj):
        return obj.students.count()

class EnrollmentRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    course_name = serializers.CharField(source='course.title', read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(source='student', read_only=True)

    class Meta:
        model = EnrollmentRequest
        fields = ['id', 'student', 'student_id', 'student_name', 'student_email', 'course', 'course_name', 'payment_proof', 'transaction_id', 'status', 'created_at']
        read_only_fields = ['student', 'status', 'created_at']
