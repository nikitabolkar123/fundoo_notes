from urllib import request
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from notes.serializers import NotesSerializer, LabelsSerializer
from notes.models import Note, Labels
from django.contrib.auth import authenticate
from rest_framework.response import Response
import user.serializers
# Logger configuration
import logging
logging.basicConfig(
    filename='exceptions.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
# Create your views here.
class NotesAPIViews(APIView):
    serializer_class=NotesSerializer
    def post(self,request):
        try:
            request.data.update({'user': request.user.id})
            serializer =NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message":"Note Created Successfully:", "data":serializer.data,"status":201},status=201)
        except Exception as e:
            logging.exception(e)
            return Response({'message':str(e)},status=400)


    def get(self,request):
        try:
            notes = Note.objects.filter(user=request.user)
            serializer = NotesSerializer(notes,many=True)
            return Response({"message":"Note Retrieve successfully","data":serializer.data,"status":201},status=201)
        except Exception as e:
            logging.exception(e)
            return Response({"message":str(e)}, status=400)


    def put(self, request,note_id):
        try:
            request.data.update({'user': request.user.id})
            notes = Note.objects.get(id=note_id)
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Notes updated successfully", "data": serializer.data, "status": 200})
        except Exception as e:
            logging.exception(e)
            return Response({'message':str(e)},status=400)

    def delete(self,request,note_id):
        try:
            notes = Note.objects.get(id=note_id)
            notes.delete()
            return Response({"message": "deleted successfully", "status": 204})
        except Exception as e:
            logging.exception(e)
            return Response({'message':str(e)},status=400)


class LabelsAPIViews(APIView):
    def post(self, request):
        try:
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Added Successfully", "data": serializer.data, "status": 201}, status=201)
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=400)

    def get(self, request):
        try:
            Labels.objects.filter(user=request.user)
            serializer = LabelsSerializer(Labels, many=True)
            return Response({"message":"Labels Retrieve successfully","data":serializer.data,"status":201},status=201)
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=400)

    def put(self, request,):
        try:
            user_id = request.data.get('user')
            # we have to update the label name so we cannot take it as unique value
            pk = request.data.get('id')
            labels = Labels.objects.get(user_id=user_id, id=pk)
            serializer = LabelsSerializer(Labels, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Labels updated successfully!', 'Data': serializer.data})
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=400)

    def delete(self, request):
        try:
            user_id = request.data.get('user')
            pk = request.data.get('id')
            labels = Labels.objects.get(user_id=user_id, id=pk)
            labels.delete()
            return Response({"Message": "Labels Deleted Successfully"}, status=204)
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=400)


class TrashNotesAPIView(APIView):
    def put(self, request, note_id):
        try:
            # note_id = request.data.get('id')
            notes = Note.objects.get(id=note_id)
            if notes.isTrash == False:
                notes.isTrash = True
            else:
                notes.isTrash = False
                return Response({'success': False, 'message': 'Notes isTrash unsuccessful!'}, status=200)
            notes.save()
            return Response({'success': True, 'message': 'Notes isTrash successful!'}, status=200)
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=400)


    def get(self, request):

        notes = Note.objects.filter(isTrash=True)
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)


class ArchiveNoteList(APIView):
    def put(self, request, note_id):
        try:
            notes = Note.objects.get(id=note_id)
            if notes.isArchive == False:
                notes.isArchive = True
            else:
                notes.isArchive = False
                return Response({'message': 'isArchived updated not successfully!'})
            notes.save()
            return Response({'message': 'isArchived updated successfully!'})
        except Exception as e:
            logging.exception(e)
            return Response({'message': str(e)}, status=400)


    def get(self, request):
        notes = Note.objects.filter(isArchive=True)
        serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)

