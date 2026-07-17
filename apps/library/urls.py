# # backend/apps/library/urls.py
# # User app URLs (basic placeholder to avoid empty urlpatterns) + (Developed by SAYAB)

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dummy_view, name='library-home'),
# ]

# File: backend/apps/library/urls.py
# Router for library (Developed by SAYAB)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookIssueViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"issues", BookIssueViewSet)

urlpatterns = [path("", include(router.urls))]
