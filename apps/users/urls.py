from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView, UserViewSet, StudentViewSet, TeacherViewSet, StaffViewSet, 
    MeView, DashboardStatsView, StudentStatsView,
    RegisterView, PendingUsersView, ApproveUserView,
    ForgotPasswordView, ResetPasswordConfirmView, ChangePasswordView
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'staff', StaffViewSet)

urlpatterns = [
    # Auth Endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'), # New
    path('me/', MeView.as_view(), name='user_me'),
    
    # Password Management Endpoints
    path('password/forgot/', ForgotPasswordView.as_view(), name='password_forgot'),
    path('password/reset/<str:uidb64>/<str:token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='password_change'),
    
    # Dashboard Stats
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('student/stats/', StudentStatsView.as_view(), name='student_stats'),

    # Admin Approval Endpoints
    path('pending-users/', PendingUsersView.as_view(), name='pending_users'),
    path('approve-user/<int:pk>/', ApproveUserView.as_view(), name='approve_user'),
    
    # ViewSets
    path('', include(router.urls)),
]
