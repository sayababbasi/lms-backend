# # from django.http import JsonResponse

# # def dummy_view(request):
# #     return JsonResponse({"message": "Result app is working"})
# # File: backend/apps/results/views.py
# # Minimal result viewset (Developed by SAYAB)

# from rest_framework import viewsets
# from .models import Result
# from .serializers import ResultSerializer

# class ResultViewSet(viewsets.ModelViewSet):
#     queryset = Result.objects.all()
#     serializer_class = ResultSerializer


# File: backend/apps/results/views.py
# Viewsets for results & transcript (Developed by SAYAB)

from rest_framework import viewsets
from .models import Result, Transcript
from .serializers import ResultSerializer, TranscriptSerializer

class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    
    def get_queryset(self):
        queryset = Result.objects.all().order_by('-created_at')
        
        # Filters
        student_id = self.request.query_params.get('student', None)
        course_id = self.request.query_params.get('course', None)
        
        if student_id:
            queryset = queryset.filter(student__id=student_id)
        if course_id:
            queryset = queryset.filter(course__id=course_id)
            
        # Permission logic: Students see their own, Staff/Teachers see all
        user = self.request.user
        if user.is_authenticated and getattr(user, 'is_student', False) and not user.is_staff:
            queryset = queryset.filter(student=user, is_blocked=False, published=True)
            
        return queryset


class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer
