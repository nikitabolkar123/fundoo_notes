from django.urls import path
from . import views

urlpatterns = [
     path('NotesAPIViews/', views.NotesAPIViews.as_view(), name = 'NotesAPIViews'),
     # path('ArchiveNotesAPIViews/', views.ArchiveNotesAPIViews.as_view(), name='ArchiveNotesAPIViews'),
     path('LabelsAPIViews/', views.LabelsAPIViews.as_view(), name='LabelsAPIViews')

]