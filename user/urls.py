from django.urls import path
from . import views

urlpatterns = [
     path('userregistration/', views.UserRegistration.as_view(), name = 'UserRegistration'),
     path('login/', views.Login.as_view(), name='login')
]  