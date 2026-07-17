# # # backend/apps/exams/urls.py
# # # User app URLs (basic placeholder to avoid empty urlpatterns) + (Developed by SAYAB)

# # from django.urls import path
# # from . import views

# # urlpatterns = [
# #     path('', views.dummy_view, name='exams-home'),
# # ]
# # File: backend/apps/exams/urls.py
# # Router for exams module (Developed by SAYAB)

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ExamViewSet, QuestionViewSet, MCQOptionViewSet

# router = DefaultRouter()
# router.register(r"", ExamViewSet)
# router.register(r"questions", QuestionViewSet)
# router.register(r"options", MCQOptionViewSet)

# urlpatterns = [path("", include(router.urls))]


# File: backend/apps/exams/urls.py
# Router for exams (Developed by SAYAB)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, QuestionViewSet, MCQOptionViewSet, StudentExamViewSet

router = DefaultRouter()
router.register(r"student", StudentExamViewSet, basename='student-exams')
router.register(r"questions", QuestionViewSet)
router.register(r"options", MCQOptionViewSet)
router.register(r"", ExamViewSet)

urlpatterns = [path("", include(router.urls))]
