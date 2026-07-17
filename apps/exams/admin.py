# # # apps/exams/admin.py
# # # Developed by SAYAB

# # from django.contrib import admin
# # from .models import Exam, Question, ExamResult

# # @admin.register(Exam)
# # class ExamAdmin(admin.ModelAdmin):
# #     list_display = ("title", "course", "scheduled_at")
# #     list_filter = ("course",)

# # @admin.register(Question)
# # class QuestionAdmin(admin.ModelAdmin):
# #     list_display = ("exam", "text", "question_type")
# #     list_filter = ("exam",)

# # @admin.register(ExamResult)
# # class ExamResultAdmin(admin.ModelAdmin):
# #     list_display = ("exam", "student", "score")
# #     list_filter = ("exam",)

# # apps/exams/admin.py
# # Developed by SAYAB

# from django.contrib import admin
# from .models import Exam, Question

# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     list_display = ("title", "course", "exam_date")  # change 'exam_date' to your field
#     list_filter = ("course", "exam_date")
#     search_fields = ("title",)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ("exam", "text", "question_type")  # ensure 'question_type' exists in Question
#     list_filter = ("question_type",)
#     search_fields = ("text",)


# File: backend/apps/exams/admin.py
# Admin registration for exams (Developed by SAYAB)

from django.contrib import admin
from .models import Exam, Question, MCQOption

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(MCQOption)
