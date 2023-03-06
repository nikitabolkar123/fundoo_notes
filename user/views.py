from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
import user
from logconfig.logger import get_logger
from user.models import User
from user.serializers import RegistrationSerializer, LoginSerializer
logger = get_logger()

# Create your views here.
class UserRegistration(APIView):
    """
       This class use to register user into the database
       """
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(request_body=RegistrationSerializer, operation_summary='Post UserRegistrations')
    def post(self, request):
        """
                   This method is used to create new user in the database.
                   :param request: It's accept first_name, last_name, email, username and password as parameter.
                   :return: It's return response that user created successfully or not.
               """
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User Registration Successfully", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary='Get Users')
    def get(self, request):
        """
       This method get all register data from the database
       """
        try:
            user = User.objects.all()
            serializer = RegistrationSerializer(user, many=True)
            return Response({"message": "Retrieve Data  Successfully", "status": 201, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
        return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    """
       This class check the user in the database
       """
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer, operation_summary='Post Login')
    def post(self, request):
        """
                   This method is used for login authentication.
                   :param request: It's accept username and password as parameter.
                   :return: It's return response that login is successful or not.
               """
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            login(request, serializer.context.get('user'))

            return Response({"message": "Login Successful", "status": 201, "data": {}}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def post(self,request):
        try:
            if request.user.is_authenticated:
                logout(request)
                return Response({"message":"Logout Successfullly"})
            else:
                return Response({"message":"Not Login" })
        except Exception as e:
            return Response({"message":"An error occured during logout:{}".format(str(e))})

