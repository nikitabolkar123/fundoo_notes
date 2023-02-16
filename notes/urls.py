from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
     path('notesapiviews/', views.NotesAPIViews.as_view(), name = 'NotesAPIViews'),
     path('notesapiviews/<int:note_id>/', views.NotesAPIViews.as_view(), name='NotesAPIViews'),
     path('archivenotelist/', views.ArchiveNoteList.as_view(), name='ArchiveNoteList'),
     path('archivenotelist/<int:note_id>/', views.ArchiveNoteList.as_view(), name='ArchiveNoteList'),
     path('labelsapiviews/', views.LabelsAPIViews.as_view(), name='labelsAPIViews'),
     path('trashnotesapiviews/', views.TrashNotesAPIView.as_view(), name='TrashNotesAPIViews'),
     path('trashnotesapiviews/<int:note_id>/', views.TrashNotesAPIView.as_view(), name='TrashNotesAPIViews')
]



# if settings.DEBUG:
#      urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#
#
