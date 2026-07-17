# admin_auth/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None or not user.is_staff:
                raise serializers.ValidationError("Invalid credentials or not an admin.")
        else:
            raise serializers.ValidationError("Username and password required.")

        data["user"] = user
        return data
