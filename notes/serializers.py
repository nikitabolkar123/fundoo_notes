from notes.models import Note
from notes.models import Labels
from rest_framework import serializers


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['label_name']
        extra_kwargs = {'user': {'required': True}}


class NotesSerializer(serializers.ModelSerializer):
    label = LabelsSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'isTrash', 'isArchive', 'image', 'color', 'label', 'reminder',
                  'collaborator']
        read_only_fields = ['label', 'collaborator']

    def create(self, validated_data):
        lable_name = self.initial_data.get("label")
        note = Note.objects.create(**validated_data)
        lable = Labels.objects.filter(label_name=lable_name)

        if lable.exists():
            note.label.add(lable.first())
            return note
        label = Labels.objects.create(label_name=lable_name, user=validated_data.get("user"))
        note.label.add(label)
        return note

#
