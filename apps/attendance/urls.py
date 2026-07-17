# # backend/apps/attendance/urls.py
# # URL patterns for Attendance app (placeholder) + (Developed by SAYAB)

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dummy_view, name='attendance-home'),
# ]


# File: backend/apps/attendance/urls.py
# Router for attendance (Developed by SAYAB)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

router = DefaultRouter()
router.register(r"", AttendanceViewSet)

urlpatterns = [path("", include(router.urls))]
