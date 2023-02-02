from urllib import request
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from Notes.serializers import NotesSerializer
from Notes.models import Note
from django.contrib.auth import authenticate
from rest_framework.response import Response
# Create your views here.
import user.serializers
from Notes.serializers import NotesSerializer
#
class NotesAPIViews(APIView):
    def post(self,request):
        serializer =NotesSerializer(data=request.data)
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

