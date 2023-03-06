from django.urls import path
from . import views

urlpatterns = [
     path('userregistration/', views.UserRegistration.as_view(), name = 'userregistration'),
     path('login/', views.Login.as_view(), name='login'),
     path('logout/', views.Logout.as_view(), name='logout')
]