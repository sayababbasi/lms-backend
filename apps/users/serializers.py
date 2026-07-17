from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Staff
from .services import PasswordService, AuditLogService, NotificationService

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 
                  'is_student', 'is_teacher', 'is_staff', 'role',
                  'phone', 'address', 'gender', 'date_of_birth', 'cnic', 'profile_picture']
        read_only_fields = ['is_staff', 'is_student', 'is_teacher', 'role']
        extra_kwargs = {
            'username': {'validators': []},
            'email': {'validators': []},
        }

    def get_role(self, obj):
        if obj.is_superuser or obj.is_staff:
            return 'admin'
        if obj.is_teacher:
            return 'teacher'
        if obj.is_student:
            return 'student'
        return 'user'

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    enrolled_courses = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'roll_number', 'department', 'program', 'semester', 'section', 
                  'guardian_name', 'guardian_contact', 'admission_date', 'enrolled_courses']

    def get_enrolled_courses(self, obj):
        return [course.title for course in obj.courses.all()]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)
        
        if not password:
            password = PasswordService.generate_secure_password()
            self._temporary_password = password
            
        user = User.objects.create_user(**user_data, password=password)
        user.is_student = True
        user.save()
        
        PasswordService.record_password_history(user, password)
        AuditLogService.log_action(user=user, action="User Created")
        NotificationService.send_welcome_email(user, password)
        
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            password = user_data.pop('password', None)
            for attr, value in user_data.items():
                setattr(user, attr, value)
            if password:
                is_valid, msg = PasswordService.validate_password_strength(password, user)
                if not is_valid:
                    raise serializers.ValidationError({"user": {"password": msg}})
                user.set_password(password)
                PasswordService.record_password_history(user, password)
                AuditLogService.log_action(user=user, action="Password Changed by Admin")
            user.save()
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if hasattr(self, '_temporary_password'):
            ret['user']['temporary_password'] = self._temporary_password
        return ret

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'department', 'designation', 'qualification', 'specialization', 'joining_date']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)
        
        if not password:
            password = PasswordService.generate_secure_password()
            self._temporary_password = password
            
        user = User.objects.create_user(**user_data, password=password)
        user.is_teacher = True
        user.save()
        
        PasswordService.record_password_history(user, password)
        AuditLogService.log_action(user=user, action="User Created")
        NotificationService.send_welcome_email(user, password)
        
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            password = user_data.pop('password', None)
            for attr, value in user_data.items():
                setattr(user, attr, value)
            if password:
                is_valid, msg = PasswordService.validate_password_strength(password, user)
                if not is_valid:
                    raise serializers.ValidationError({"user": {"password": msg}})
                user.set_password(password)
                PasswordService.record_password_history(user, password)
                AuditLogService.log_action(user=user, action="Password Changed by Admin")
            user.save()
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if hasattr(self, '_temporary_password'):
            ret['user']['temporary_password'] = self._temporary_password
        return ret

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Staff
        fields = ['id', 'user', 'role', 'designation', 'joining_date']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)
        
        if not password:
            password = PasswordService.generate_secure_password()
            self._temporary_password = password
            
        user = User.objects.create_user(**user_data, password=password)
        user.save()
        
        PasswordService.record_password_history(user, password)
        AuditLogService.log_action(user=user, action="User Created")
        NotificationService.send_welcome_email(user, password)
        
        staff = Staff.objects.create(user=user, **validated_data)
        return staff

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            password = user_data.pop('password', None)
            for attr, value in user_data.items():
                setattr(user, attr, value)
            if password:
                is_valid, msg = PasswordService.validate_password_strength(password, user)
                if not is_valid:
                    raise serializers.ValidationError({"user": {"password": msg}})
                user.set_password(password)
                PasswordService.record_password_history(user, password)
                AuditLogService.log_action(user=user, action="Password Changed by Admin")
            user.save()
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if hasattr(self, '_temporary_password'):
            ret['user']['temporary_password'] = self._temporary_password
        return ret
