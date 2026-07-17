# # # backend/apps/results/urls.py
# # # User app URLs (basic placeholder to avoid empty urlpatterns) + (Developed by SAYAB)

# # from django.urls import path
# # from . import views

# # urlpatterns = [
# #     path('', views.dummy_view, name='results-home'),
# # ]

# # File: backend/apps/results/urls.py
# # Router for results (Developed by SAYAB)

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ResultViewSet

# router = DefaultRouter()
# router.register(r"", ResultViewSet)

# urlpatterns = [path("", include(router.urls))]


# File: backend/apps/results/urls.py
# Router for results (Developed by SAYAB)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResultViewSet, TranscriptViewSet

router = DefaultRouter()
router.register(r"", ResultViewSet, basename="result")
router.register(r"transcripts", TranscriptViewSet)

urlpatterns = [path("", include(router.urls))]
