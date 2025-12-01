
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, AuthenticationFailed, ValidationError
from account.models import User
from account.serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from account.auth_utils import token_generation







class Login(APIView):
    def get(self,request):
        account = User.objects.filter(email= request.data["email"]).first()
        if not account:
            raise NotFound("User Not Found") 
        if not check_password(request.data["password"],account.password):
            raise AuthenticationFailed("Invalid Password")
        token = token_generation(account)        
        return Response({
                "message": "Logged In Successfully",
                "token": token,
                "user_id": account.id,
                "username": account.username
            },
            status=status.HTTP_200_OK
        )


class CreateUser(APIView):
    def post(self, request):
        user_data =  request.data
        if not user_data:
            raise NotFound("Data Not Found")
        if "password" in user_data:
            user_data["password"] = make_password(user_data["password"])
        serializer = UserSerializer(data=user_data)
        if not serializer.is_valid():
            raise ValidationError("Data is not valid")
        serializer.save()
        return Response("User created",status=status.HTTP_200_OK)
    
    