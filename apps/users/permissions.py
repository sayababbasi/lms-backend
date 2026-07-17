from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow Admins (is_staff=True).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow Teachers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher)

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow Students.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)
