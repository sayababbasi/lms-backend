from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .services.youtube_service import YouTubeService
from .models import Lesson

from rest_framework.permissions import IsAdminUser

class YouTubeAuthView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only Super Admin can connect a YouTube account.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            auth_url = YouTubeService.get_auth_url()
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(auth_url)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class YouTubeAuthCallbackView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only Super Admin can connect a YouTube account.'}, status=status.HTTP_403_FORBIDDEN)
        
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'No authorization code provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            tokens = YouTubeService.get_tokens(code)
            return Response({
                'message': 'Successfully authenticated. Please add YOUTUBE_REFRESH_TOKEN to your .env file.',
                'refresh_token': tokens['refresh_token']
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import os
import tempfile
from rest_framework.parsers import MultiPartParser, FormParser

class YouTubeUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        user = request.user
        if not user.is_authenticated or not (user.is_teacher or user.is_superuser):
            return Response({'error': 'Only instructors or admins can upload lectures.'}, status=status.HTTP_403_FORBIDDEN)

        file_obj = request.FILES.get('video')
        lesson_id = request.data.get('lessonId')
        title = request.data.get('title', 'LMS Lecture')
        description = request.data.get('description', '')

        if not file_obj:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve lesson if ID provided
        lesson = None
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
            except Lesson.DoesNotExist:
                return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

        if lesson:
            lesson.upload_status = 'processing'
            lesson.save()

        # Save uploaded file to temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        try:
            for chunk in file_obj.chunks():
                temp_file.write(chunk)
            temp_file.close()

            # Dispatch Celery Task
            from .tasks import process_youtube_upload
            process_youtube_upload.delay(temp_file.name, title, description, lesson_id)

            return Response({
                'message': 'Upload processing started in the background.',
                'status': 'processing'
            }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            if lesson:
                lesson.upload_status = 'failed'
                lesson.save()
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
