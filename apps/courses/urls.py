from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, LessonViewSet, ResourceViewSet, EnrollmentRequestViewSet, StudentCoursesView
from .youtube_views import YouTubeAuthView, YouTubeAuthCallbackView, YouTubeUploadView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'enrollment-requests', EnrollmentRequestViewSet)

urlpatterns = [
    path('student/courses/', StudentCoursesView.as_view(), name='student-courses'),
    path('auth/youtube/', YouTubeAuthView.as_view(), name='youtube-auth'),
    path('auth/youtube/callback/', YouTubeAuthCallbackView.as_view(), name='youtube-auth-callback'),
    path('youtube/upload/', YouTubeUploadView.as_view(), name='youtube-upload'),
    path('', include(router.urls)),
]
