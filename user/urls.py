from django.urls import path
from . import views

urlpatterns = [
     path('userregistration/', views.UserRegistration.as_view(), name = 'User_registration'),
     path('', views.Login.as_view(), name='login'),
     path('logout/', views.Logout.as_view(), name='user_logout'),
     # path('login_template/', views.LoginTemplate.as_view(), name='loginview')
]