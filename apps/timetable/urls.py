# # backend/apps/timetable/urls.py
# # User app URLs (basic placeholder to avoid empty urlpatterns) + (Developed by SAYAB)

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dummy_view, name='timetable-home'),
# ]

# File: backend/apps/timetable/urls.py
# Router for timetable (Developed by SAYAB)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeSlotViewSet

router = DefaultRouter()
router.register(r"", TimeSlotViewSet, basename="timeslot")

urlpatterns = [path("", include(router.urls))]
