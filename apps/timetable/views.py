# from django.http import JsonResponse

# def dummy_view(request):
#     return JsonResponse({"message": "Timetable app is working"})

# File: backend/apps/timetable/views.py
# Timetable viewset (Developed by SAYAB)

from rest_framework import viewsets
from .models import TimeSlot
from .serializers import TimeSlotSerializer

class TimeSlotViewSet(viewsets.ModelViewSet):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        queryset = TimeSlot.objects.all()
        
        # Filter by day
        day = self.request.query_params.get('day', None)
        if day:
            queryset = queryset.filter(day=day)

        # For students, only show courses they are enrolled in
        user = self.request.user
        if hasattr(user, 'is_student') and user.is_student:
             # Assuming Student model has related name 'student_profile' or similar
             # But simplified: check enrollment via Student model
             # Students see timeslots for courses they are enrolled in
             if hasattr(user, 'student_profile'):
                 enrolled_courses = user.student_profile.courses.all()
                 queryset = queryset.filter(course__in=enrolled_courses)

        # For teachers, show their own classes + optionally all (admin view)
        if hasattr(user, 'is_teacher') and user.is_teacher:
             # Teacher sees their own classes by default? 
             # Actually, teacher might want to see full schedule or just theirs.
             # For now, let's show all for teachers/admins so they can manage.
             pass

        return queryset
