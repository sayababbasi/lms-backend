# # # # # apps/users/admin.py
# # # # # Developed by SAYAB

# # # # from django.contrib import admin
# # # # from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# # # # from .models import User, Student, Teacher, Staff

# # # # @admin.register(User)
# # # # class UserAdmin(BaseUserAdmin):
# # # #     list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
# # # #     search_fields = ("username", "email")
# # # #     list_filter = ("is_staff", "is_superuser", "is_active")
# # # #     ordering = ("username",)

# # # # @admin.register(Student)
# # # # class StudentAdmin(admin.ModelAdmin):
# # # #     list_display = ("user", "roll_number", "course")
# # # #     search_fields = ("user__username", "roll_number")

# # # # @admin.register(Teacher)
# # # # class TeacherAdmin(admin.ModelAdmin):
# # # #     list_display = ("user", "department")
# # # #     search_fields = ("user__username", "department")

# # # # @admin.register(Staff)
# # # # class StaffAdmin(admin.ModelAdmin):
# # # #     list_display = ("user", "role")
# # # #     search_fields = ("user__username", "role")


# # # # apps/users/admin.py
# # # # Developed by SAYAB

# # # from django.contrib import admin
# # # from .models import Student, Teacher

# # # @admin.register(Student)
# # # class StudentAdmin(admin.ModelAdmin):
# # #     list_display = ("user", "roll_number", "department")  # ensure fields exist
# # #     search_fields = ("user__username", "roll_number")

# # # @admin.register(Teacher)
# # # class TeacherAdmin(admin.ModelAdmin):
# # #     list_display = ("user", "department")
# # #     search_fields = ("user__username",)
# # # File: backend/apps/users/admin.py
# # # Admin registration for User model (Developed by SAYAB)

# # from django.contrib import admin
# # from django.contrib.auth import get_user_model
# # from django.contrib.auth.admin import UserAdmin

# # User = get_user_model()

# # @admin.register(User)
# # class CustomUserAdmin(UserAdmin):
# #     fieldsets = UserAdmin.fieldsets + (
# #         (None, {"fields": ("is_student", "is_teacher", "phone")}),
# #     )
# #     list_display = ("username", "email", "is_student", "is_teacher", "is_staff")


# # File: backend/apps/users/admin.py
# # Admin registration for users app (Developed by SAYAB)

# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin
# from .models import Student, Teacher, Staff

# User = get_user_model()

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {"fields": ("is_student","is_teacher","phone")}),
#     )
#     list_display = ("username"  ,"email","is_student","is_teacher","is_staff")

# admin.site.register(Student)
# admin.site.register(Teacher)
# admin.site.register(Staff)


# backend/apps/users/admin.py
# Admin registration for User, Student, Teacher, Staff (Developed by SAYAB)

from django.contrib import admin
from .models import User, Student, Teacher, Staff

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher', 'is_staff')
    list_filter = ('is_student', 'is_teacher', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department')
    search_fields = ('user__username', 'roll_number', 'department')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
