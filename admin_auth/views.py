# admin_auth/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from .serializers import AdminLoginSerializer

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response({"message": "Admin logged in successfully."})

class AdminLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Admin logged out successfully."})
