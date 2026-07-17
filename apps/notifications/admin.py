# # # apps/notifications/admin.py
# # # Developed by SAYAB

# # from django.contrib import admin
# # from .models import Notification

# # @admin.register(Notification)
# # class NotificationAdmin(admin.ModelAdmin):
# #     list_display = ("recipient", "message", "created_at", "notification_type")  # ensure fields exist
# #     list_filter = ("notification_type",)
# #     search_fields = ("message", "recipient__username")


# # apps/notifications/admin.py
# # Developed by SAYAB

# from django.contrib import admin
# from .models import Notification

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     # Use actual fields from Notification model
#     list_display = (
#         "id",
#         "recipient_student",
#         "recipient_teacher",
#         "message",
#         "notification_type",
#         "created_at",
#     )
#     list_filter = ("notification_type",)
#     search_fields = (
#         "recipient_student__user__username",
#         "recipient_teacher__user__username",
#         "message",
#     )


# File: backend/apps/notifications/admin.py
# Admin registration for notifications (Developed by SAYAB)

from django.contrib import admin
from .models import Notification

admin.site.register(Notification)
