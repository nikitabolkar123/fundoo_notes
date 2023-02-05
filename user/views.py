from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from user.models import User
from user.serializers import RegistrationSerializer,LoginSerializer

# Create your views here.
class UserRegistration(APIView):

    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User Registration Successfully", "data": serializer.data, "status": 201},status=201)
class Login(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message":"login successful"})
        except Exception as e:

            return Response({"message":e.args[0]})
#
