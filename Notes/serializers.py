from Notes.models import Note
from Notes.models import Labels
from rest_framework import serializers

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user','title','content','created_at','updated_at']
#
    def create(self, validated_data):
        print(validated_data)
        print(self.context)
        lable_name=self.context[0]
        note=Note.objects.create(**validated_data)
        lable=Labels.objects.filter(name=lable_name)
        if lable.exists():
            note.label.add(lable.first())
            return note
        label=Labels.objects.create(name=lable_name,user=validated_data.get("user"))
        note.label.add(label)
        return  note

#


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields=['name','user']
        # fields = ['id', 'user','title','content','created_at','updated_at',]