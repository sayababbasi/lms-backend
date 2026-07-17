from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, SubmissionViewSet, GradeViewSet, CourseAssignmentStatsViewSet, StudentAssignmentListView, AssignmentSubmissionView

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'assignment-stats', CourseAssignmentStatsViewSet, basename='course-stats')

urlpatterns = [
    path('assignments/student/list/', StudentAssignmentListView.as_view(), name='student-assignments-list'),
    path('assignments/student/<int:pk>/submit/', AssignmentSubmissionView.as_view(), name='student-assignment-submit'),
    path('', include(router.urls)),
]
