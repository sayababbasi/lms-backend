# File: backend/apps/library/serializers.py
# Serializers for library (Developed by SAYAB)

from rest_framework import serializers
from .models import Book, BookIssue

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = "__all__"
