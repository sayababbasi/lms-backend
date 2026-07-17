# # backend/apps/notification/urls.py
# # User app URLs (basic placeholder to avoid empty urlpatterns) + (Developed by SAYAB)

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dummy_view, name='notification-home'),
# ]

# File: backend/apps/notifications/urls.py
# Router for notifications (Developed by SAYAB)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"logs", NotificationViewSet) # Changed from notifications to logs for clarity
router.register(r"messages", MessageViewSet)

urlpatterns = [path("", include(router.urls))]
