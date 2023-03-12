from django.urls import path
from . import views

urlpatterns = [
     # path('userregistration/', views.UserRegistration.as_view(), name = 'User_registration'),
     # path('', views.Login.as_view(), name='login'),
     # path('logout/', views.Logout.as_view(), name='user_logout'),
     path('', views.UserLogin.as_view(), name='login'),
     path('register/', views.UserRegistrationTemp.as_view(), name='register'),
     path('profile/', views.User_Profile.as_view(), name='profile'),
     path('logout/', views.UserLogout.as_view(), name='logout')
]
#      path('login_template/', views.LoginTemplate.as_view(), name='loginview'),
#      path('registration_template/', views.UserRegistrationTemp.as_view(), name='registerview'),
#      path('userprofile/', views.UserProfile.as_view(), name='User_Profile')
# ]
