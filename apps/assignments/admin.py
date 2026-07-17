# # apps/assignments/admin.py
# # Developed by SAYAB

# from django.contrib import admin
# from .models import Assignment, Submission, Grade

# @admin.register(Assignment)
# class AssignmentAdmin(admin.ModelAdmin):
#     list_display = ("title", "course", "due_date")
#     search_fields = ("title",)
#     list_filter = ("course", "due_date")

# @admin.register(Submission)
# class SubmissionAdmin(admin.ModelAdmin):
#     list_display = ("assignment", "student", "submitted_at")
#     list_filter = ("assignment",)

# @admin.register(Grade)
# class GradeAdmin(admin.ModelAdmin):
#     list_display = ("submission", "marks", "graded_by")  # make sure 'graded_by' exists in your Grade model
#     list_filter = ("graded_by",)


# File: backend/apps/assignments/admin.py
# Admin registration for assignments (Developed by SAYAB)

from django.contrib import admin
from .models import Assignment, Submission, Grade

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Grade)
