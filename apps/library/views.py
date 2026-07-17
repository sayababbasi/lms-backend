# from django.http import JsonResponse

# def dummy_view(request):
#     return JsonResponse({"message": "Library app is working"})

# File: backend/apps/library/views.py
# Viewsets for library (Developed by SAYAB)

from rest_framework import viewsets
from .models import Book, BookIssue
from .serializers import BookSerializer, BookIssueSerializer

from rest_framework.parsers import MultiPartParser, FormParser

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-uploaded_at')
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, FormParser)

class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
