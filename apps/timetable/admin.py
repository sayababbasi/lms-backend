# # # apps/timetable/admin.py
# # # Developed by SAYAB

# # from django.contrib import admin
# # from .models import Timetable

# # @admin.register(Timetable)
# # class TimetableAdmin(admin.ModelAdmin):
# #     list_display = ("course", "day", "start_time", "end_time")
# #     list_filter = ("day", "course")
# # apps/timetable/admin.py
# # Developed by SAYAB

# from django.contrib import admin
# from .models import TimeSlot, TimetableEntry, StudentTimetable

# @admin.register(TimeSlot)
# class TimeSlotAdmin(admin.ModelAdmin):
#     list_display = ('start_time', 'end_time')
#     ordering = ('start_time',)
#     search_fields = ('start_time', 'end_time')

# @admin.register(TimetableEntry)
# class TimetableEntryAdmin(admin.ModelAdmin):
#     list_display = ('course', 'teacher', 'day', 'timeslot', 'room')
#     list_filter = ('day', 'teacher', 'course')
#     search_fields = ('course__name', 'teacher__user__username', 'room')

# @admin.register(StudentTimetable)
# class StudentTimetableAdmin(admin.ModelAdmin):
#     list_display = ('student', 'timetable_entry')
#     list_filter = ('timetable_entry__day', 'timetable_entry__course')
#     search_fields = ('student__user__username', 'timetable_entry__course__name')


# File: backend/apps/timetable/admin.py
# Admin registration for timetable (Developed by SAYAB)

from django.contrib import admin
from .models import TimeSlot

admin.site.register(TimeSlot)
