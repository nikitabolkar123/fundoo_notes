from rest_framework import serializers
from notes.models import Labels
from notes.models import Note
from user.models import User


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
        collab_data = self.initial_data.get('collaborator')
        v_user = validated_data.get("user")
        if collab_data is not None:
            for data in collab_data:
                try:
                    user = User.objects.get(username=data)
                    if v_user != user:
                        note.collaborator.add(user)
                except:
                    pass

        if lable_name is not None:
            for l in lable_name:
                lable = Labels.objects.filter(label_name=l, user=v_user)
                if lable.exists():
                    note.label.add(lable.first())
                    # return note
                else:
                    lab = Labels.objects.create(label_name=l, user=v_user)  # user=validated_data.get("user"))
                    note.label.add(lab)
        return note
