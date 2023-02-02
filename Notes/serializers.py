from Notes.models import Note
from Notes.models import Labels
from rest_framework import serializers

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user','title','content','created_at','updated_at','collaborator','label','isArchieve','isTrash','color',
                  'reminder','image']

class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['id', 'user','title','content','created_at','updated_at',]