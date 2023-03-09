from django.urls import path
from . import views

urlpatterns = [
    path('notesapiviews/', views.NotesAPIViews.as_view(), name='notesapiviews'),
    path('notesapiviews/<int:note_id>/', views.NotesAPIViews.as_view(), name='notes_apiviews'),
    path('archivenotelist/', views.ArchiveNoteList.as_view(), name='ArchiveNoteList'),
    path('archivenotelist/<int:note_id>/', views.ArchiveNoteList.as_view(), name='ArchiveNoteList'),
    path('labelsapiviews/', views.LabelsAPIViews.as_view(), name='labelsAPIViews'),
    path('labelsapiviews/<str:label_name>/', views.LabelsAPIViews.as_view(), name='labels_APIViews'),
    path('trashnotesapiviews/', views.TrashNotesAPIView.as_view(), name='TrashNotesAPIViews'),
    path('trashnotesapiviews/<int:note_id>/', views.TrashNotesAPIView.as_view(), name='TrashNotesAPIViews'),
    path('notescollaborator/', views.NotesCollaboratorAPIViews.as_view(), name='NotesCollaboratorAPIViews'),
    # path('notescollaborator/<int:note_id>/<int:user_id>/', views.NotesCollaboratorAPIViews.as_view(), name='NotesCollaboratorAPIViews'),
    path('notes_collaborator/<int:note_id>/', views.NotesCollaboratorAPIViews.as_view(),name='NotesCollaboratorAPIViews'),
    # path('notes_collaborator/<int:note_id>/collaborator/<str:collaborator_username>/', views.NotesCollaboratorAPIViews.as_view(), name='NotesCollaboratorAPIViews'),

]
