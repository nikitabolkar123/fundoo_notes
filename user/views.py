from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View
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

#
class UserRegistrationTemp(View):
    @csrf_exempt
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phnno = request.POST.get('phnno')
            city = request.POST.get('city')
            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name, email=email, phnno=phnno, city=city)
            messages.success(request,"Your account has been created successfully")
            return redirect('login')
        except Exception as e:
            logger.exception(e)
            return render(request, 'user/registration.html')

    def get(self, request):
        return render(request, 'user/registration.html')


class UserLogin(View):
    name_of_template = 'user/login.html'
    @method_decorator(sensitive_post_parameters('password'))
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, self.name_of_template)
        except Exception as e:
            logger.exception(e)
            return render(request, self.name_of_template)

    def get(self, request):
        return render(request, self.name_of_template) #render login.html page


class User_Profile(View):
    def get(self, request):
        context = {'heading': "Hey.....WELCOME TO FUNDOO NOTE", 'user': request.user}
        return render(request, 'user/user_profile.html', context)
class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # it will redirect to login page
