from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from logconfig.logger import get_logger
from user.models import User
from user.serializers import RegistrationSerializer, LoginSerializer

logger = get_logger()


# Create your views here.
class UserRegistration(APIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(request_body=RegistrationSerializer, operation_summary='Post UserRegistrations')
    def post(self, request):
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
        try:
            user = User.objects.all()
            serializer = RegistrationSerializer(user, many=True)
            return Response({"message": "Retrieve Data  Successfully", "status": 201, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
        return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer, operation_summary='Post Login')
    def post(self, request):

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
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"Message": "Logout Successfully"})
        return Response({"Message": "User already logout"})
