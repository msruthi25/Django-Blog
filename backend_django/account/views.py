from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from backend_django.account.serializers import UserCreateSerializer, UserLoginSerializer
from .tasks import welcome_task

class CreateUser(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            welcome_task.delay(user.username)
            messages.success(
                request,
                "Account created successfully! Please login."
            )
            return redirect("posts")

        for field, errors in serializer.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return redirect("posts")


class Login(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("posts")

        for field, errors in serializer.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return redirect("posts")


class Logout(APIView):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect("posts")
