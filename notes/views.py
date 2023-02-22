from urllib import request
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from django.shortcuts import render
from rest_framework.views import APIView
from logconfig.logger import get_logger
from notes.serializers import NotesSerializer, LabelsSerializer
from notes.models import Note, Labels
from django.contrib.auth import authenticate
from rest_framework.response import Response
import user.serializers

# Logger configuration
logger = get_logger()


# Create your views here.
class NotesAPIViews(APIView):
    """
          NotesAPIView : POST ,GET, UPDATE, DELETE Notes
    """
    serializer_class = NotesSerializer

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='POST Notes')
    def post(self, request):
        """
              This method create note for user
        """
        try:
            request.data.update({'user': request.user.id})
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Created Successfully", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary='Get Notes')
    def get(self, request):
        """
            This method get notes for user
        """
        try:
            notes = Note.objects.filter(user=request.user)
            serializer = NotesSerializer(notes, many=True)
            return Response({"message": "Note Retrieved Successfully", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='Put Notes')
    def put(self, request, note_id):
        """
            This method update note for user
        """
        try:
            request.data.update({'user': request.user.id})
            notes = Note.objects.get(id=note_id)
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Updated Successfully", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='Delete Notes')
    def delete(self, request, note_id):
        """
            This method delete note for user
        """
        try:
            notes = Note.objects.get(id=note_id)
            notes.delete()
            return Response({"message": "Note Deleted Successfully", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class LabelsAPIViews(APIView):
    """
            LabelsAPIView : GET, ADD, UPDATE, DELETE Labels
    """
    serializer_class = LabelsSerializer

    @swagger_auto_schema(request_body=LabelsSerializer, operation_summary='Post Label')
    def post(self, request):
        """
            This method is create label for user
        """
        try:
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response({"message": "Label Created Successfully", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary='Get Label')
    def get(self, request):
        try:
            labels = Labels.objects.filter(user=request.user)
            serializer = LabelsSerializer(labels, many=True)
            return Response({"message": "Data Retrieved Successfully", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LabelsSerializer, operation_summary='Put Label')
    def put(self, request, label_name):
        try:
            label = Labels.objects.get(label_name=label_name, user=request.user)
            serializer = LabelsSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Updated Successfully", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LabelsSerializer, operation_summary='Delete Label')
    def delete(self, request, label_name):
        try:
            labels = Labels.objects.get(label_name=label_name, user=request.user)
            labels.delete()
            return Response({"message": "Label Deleted Successfully", "status": 204, "data": {}},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class TrashNotesAPIView(APIView):
    """
          TrashNotesAPIView: Trash notes And Restore notes.
    """
    serializer_class = NotesSerializer

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='Delete Label')
    def put(self, request, note_id):
        try:
            notes = Note.objects.get(id=note_id)
            if notes.isTrash == False:
                notes.isTrash = True
            else:
                notes.isTrash = False
                return Response({'success': False, 'message': 'Notes isTrash unsuccessful!'}, status=200)
            notes.save()
            return Response({'success': True, 'message': 'Notes isTrash successful!'}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=400)

    @swagger_auto_schema(operation_summary='Get TrashNote ')
    def get(self, request):
        try:
            notes = Note.objects.filter(isTrash=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({"message": "Data Retrieved Successfully", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
        return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class ArchiveNoteList(APIView):
    """
          ArchiveNotesAPIView: Archive & UnArchive notes.
    """
    serializer_class = NotesSerializer

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='Put Archive Note')
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
            logger.exception(e)
            return Response({'message': str(e)}, status=400)

    @swagger_auto_schema(operation_summary='Get Archive Note ')
    def get(self, request):
        try:
            notes = Note.objects.filter(isArchive=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({"message": "Data Retrieved Successfully", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
        return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
