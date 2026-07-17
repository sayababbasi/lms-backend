from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def root_api(request):
    """
    Root API view listing all available apps and their main endpoints.
    """
    data = {
        "message": "Welcome to Revotic LMS Backend API!",
        "version": "1.0.0",
        "docs": "/docs/",
        "admin_panel": "/admin/",
        "api_root": "/api/"
    }
    return JsonResponse(data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_api, name='root-api'),
    
    # API Routes
    path('api/', include('apps.users.urls')), # Includes users, students, teachers, auth
    
    # Placeholder for other apps (will uncomment as I implement them)
    path('api/', include('apps.courses.urls')),
    path('api/', include('apps.assignments.urls')),
    # path('api/assignments/', include('apps.assignments.urls')),
    path('api/exams/', include('apps.exams.urls')),
    path('api/results/', include('apps.results.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/library/', include('apps.library.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/timetable/', include('apps.timetable.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
