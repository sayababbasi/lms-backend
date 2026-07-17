# # # apps/results/admin.py
# # # Developed by SAYAB

# # from django.contrib import admin
# # from .models import Result, Transcript, GPA

# # @admin.register(Result)
# # class ResultAdmin(admin.ModelAdmin):
# #     list_display = ("student", "course", "marks_obtained")
# #     list_filter = ("course",)

# # @admin.register(GPA)
# # class GPAAdmin(admin.ModelAdmin):
# #     list_display = ("student", "gpa", "semester")

# # @admin.register(Transcript)
# # class TranscriptAdmin(admin.ModelAdmin):
# #     list_display = ("student", "created_at")


# # apps/results/admin.py
# # Developed by SAYAB

# from django.contrib import admin
# from .models import Result, Transcript

# @admin.register(Result)
# class ResultAdmin(admin.ModelAdmin):
#     list_display = ("student", "course", "marks_obtained")  # ensure these fields exist
#     list_filter = ("course",)

# @admin.register(Transcript)
# class TranscriptAdmin(admin.ModelAdmin):
#     list_display = ("student", "created_at")  # ensure these fields exist
#     list_filter = ("created_at",)


# File: backend/apps/results/admin.py
# Admin registration for results (Developed by SAYAB)

from django.contrib import admin
from .models import Result, Transcript

admin.site.register(Result)
admin.site.register(Transcript)
