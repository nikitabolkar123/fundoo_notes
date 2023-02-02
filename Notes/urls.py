from django.urls import path
from . import views

urlpatterns = [
     path('NotesAPIViews/', views.NotesAPIViews.as_view(), name = 'NotesAPIViews'),
    # path('Login/', views.Login.as_view(), name='Login'),

]