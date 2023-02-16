from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from user.models import User
from user.serializers import RegistrationSerializer,LoginSerializer

# Create your views here.
class UserRegistration(APIView):
    serializer_class=RegistrationSerializer

    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User Registration Successfully", "data": serializer.data, "status": 201},status=201)

    def get(self, request):
        user = User.objects.all()
        serializer = RegistrationSerializer(user, many=True)
        return Response(serializer.data)
class Login(APIView):
    serializer_class=LoginSerializer

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            login(request, serializer.context.get('user'))
            return Response({"message":"login successful"},status=201)
        except Exception as e:
            return Response({"message":e.args[0]})
#


