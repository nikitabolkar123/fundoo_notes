from urllib import request
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from Notes.serializers import NotesSerializer, LabelsSerializer
from Notes.models import Note, Labels
from django.contrib.auth import authenticate
from rest_framework.response import Response
import user.serializers


# Create your views here.
class NotesAPIViews(APIView):
    def post(self,request):
        print(request.data)
        serializer =NotesSerializer(data=request.data,context=request.data.get('label'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Registered Successfully:", "data":serializer.data,"status":201},status=201)


    def get(self,request):
        try:
            user_id= request.query_params.get('user_id')
            notes=Note.objects.filter(user_id=user_id)
            serializer = NotesSerializer(notes,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message":str(e)}, status=400)


    def put(self, request):
        try:
            user_id = request.data.get('user')
            mk = request.data.get('id')
            notes = Note.objects.get(id=mk,user_id=user_id)
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "updated successfully", "data": serializer.data, "status": 200})
        except Exception as e:
            return Response({'message':str(e)},status=400)

    def delete(self,request):
        try:
            user_id = request.data.get('user')
            pk = request.data.get('id')
            notes = Note.objects.get(user_id=user_id,id=pk)
            notes.delete()
            return Response({"message": "deleted successfully", "status": 204})
        except Exception as e:
            return Response({'message':str(e)},status=400)

print('*******************************************************')
class LabelsAPIViews(APIView):
    def post(self, request):
        try:
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Added Successfully", "data": serializer.data, "status": 201}, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def get(self, request):
        try:
            user_id = request.data.get('user')
            labels = Labels.objects.filter(user=user_id)
            serializer = LabelsSerializer(labels, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def put(self, request):
        try:
            user_id = request.data.get('user')
            # we have to update the label name so we cannot take it as unique value
            pk = request.data.get('id')
            labels = Labels.objects.get(user_id=user_id, id=pk)
            serializer = LabelsSerializer(labels, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Labels updated successfully!', 'Data': serializer.data})

        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def delete(self, request):
        try:
            user_id = request.data.get('user')
            pk = request.data.get('id')
            labels = Labels.objects.get(user_id=user_id, id=pk)
            labels.delete()
            return Response({"Message": "Labels Deleted Successfully"}, status=204)
        except Exception as e:
            return Response({'message': str(e)}, status=400)















