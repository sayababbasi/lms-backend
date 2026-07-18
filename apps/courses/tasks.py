from celery import shared_task
from .services.youtube_service import YouTubeService
from .models import Lesson
import os
from django.utils import timezone

@shared_task
def process_youtube_upload(temp_file_path, title, description, lesson_id=None):
    lesson = None
    if lesson_id:
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            pass

    try:
        # Upload to YouTube
        video_id = YouTubeService.upload_video(temp_file_path, title, description)
        embed_url = f"https://www.youtube.com/embed/{video_id}"

        # Update Lesson
        if lesson:
            lesson.youtube_video_id = video_id
            lesson.youtube_embed_url = embed_url
            lesson.upload_status = 'completed'
            lesson.uploaded_at = timezone.now()
            lesson.save()

    except Exception as e:
        if lesson:
            lesson.upload_status = 'failed'
            lesson.save()
        raise e
    finally:
        # Always clean up the temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
