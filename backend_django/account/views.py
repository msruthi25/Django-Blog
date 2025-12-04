
from rest_framework.response import Response
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, AuthenticationFailed, ValidationError
from account.models import User
from account.serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from account.auth_utils import token_generation
from django.contrib import messages

class Login(APIView):
    def post(self,request):
        account = User.objects.filter(email= request.data["email"]).first()
        if not account:
            raise NotFound("User Not Found") 
        if not check_password(request.data["password"],account.password):
            raise AuthenticationFailed("Invalid Password")
        token = token_generation(account) 
        response = redirect("posts")  
        response.set_cookie(key="access_token",value=token,httponly=True,samesite="Lax")
        response.set_cookie(key="username",value=account.username,samesite="Lax")
        response.set_cookie(key="user_id",value=account.id,samesite="Lax")        
        return response


class CreateUser(APIView):
    def post(self, request):
        user_data =  request.POST.copy()
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")
        if not username or not email or not password:
            raise NotFound("Missing Fields")
        if password:
            user_data["password"] = make_password(password)
        serializer = UserSerializer(data=user_data)
        if not serializer.is_valid():
            raise ValidationError("Data is not valid")
        serializer.save()
        messages.success(request, "Account created successfully! Login to view your Account")
        response = redirect("posts") 
        return response



class Logout(APIView):
    def get(self,request):
        response = redirect("posts") 
        response.delete_cookie("access_token")
        response.delete_cookie("username")
        response.delete_cookie("user_id")
        return response        
    
    