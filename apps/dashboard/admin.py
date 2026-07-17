# apps/dashboard/admin.py
# Developed by SAYAB

from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from apps.users.models import User, Student, Teacher, Staff
from apps.courses.models import Course
from apps.assignments.models import Assignment
from apps.exams.models import Exam
from apps.results.models import Result

class DashboardAdminSite(admin.AdminSite):
    site_header = "Revotic AI LMS Administration"
    site_title = "Revotic AI LMS Portal"
    index_title = "Welcome to Revotic AI LMS Backend"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard))
        ]
        return custom_urls + urls

    def dashboard(self, request):
        context = dict(
            self.each_context(request),
            total_users=User.objects.count(),
            total_students=Student.objects.count(),
            total_teachers=Teacher.objects.count(),
            total_courses=Course.objects.count(),
            total_assignments=Assignment.objects.count(),
            total_exams=Exam.objects.count(),
            total_results=Result.objects.count(),
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

# Replace default admin site
admin_site = DashboardAdminSite(name='dashboard')
