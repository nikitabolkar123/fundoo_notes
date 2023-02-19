from django.contrib.auth import authenticate, login
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.views import APIView
from user.models import User
from user.serializers import RegistrationSerializer,LoginSerializer
import logging
logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

# Create your views here.
class UserRegistration(APIView):
    """
       This class use to register user into the database
       """

    serializer_class=RegistrationSerializer
    @swagger_auto_schema(request_body=RegistrationSerializer, operation_summary='POST Notes')
    def post(self,request):
        """
                   This method is used to create new user in the database.
                   :param request: It's accept first_name, last_name, email, username and password as parameter.
                   :return: It's return response that user created successfully or not.
               """
        try:
            serializer=RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User Registration Successfully", "status": 201, "data": serializer.data},status=status.HTTP_201_CREATED)
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
        return Response({"message": "Retrieve Data  Successfully", "status": 201, "data": serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    """
       This class check the user in the database
       """
    serializer_class=LoginSerializer
    @swagger_auto_schema(request_body=LoginSerializer, operation_summary='POST Method')
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
            return Response({"message": "Login Successful", "status": 202, "data": {}},status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)



