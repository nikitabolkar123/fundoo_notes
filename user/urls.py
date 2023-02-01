from django.urls import path
from . import views

urlpatterns = [
     path('UserRegistration/', views.UserRegistration.as_view(), name = 'UserRegistration'),
     path('Login/', views.Login.as_view(), name='Login'),
]