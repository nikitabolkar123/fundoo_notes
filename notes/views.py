from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from logconfig.logger import get_logger
from notes.models import Note, Labels
from notes.serializers import NotesSerializer, LabelsSerializer
from user.models import User
from .utils import RedisCrud

# Logger configuration
logger = get_logger()


# Create your views here.
class NotesAPIViews(APIView):
    """
          NotesAPIView : POST ,GET, UPDATE, DELETE Notes
    """
    serializer_class = NotesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
            RedisCrud().save(serializer.data, request.user.id)
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
            # redis_data = RedisCrud().retrieve(request.user)
            # if redis_data:
            #     return Response({"message": "Note Retrieved Successfully", "status": 200, "data": redis_data},
            #                     status=status.HTTP_200_OK)
            notes = Note.objects.filter(Q(user__id=request.user.id) | Q(collaborator__id=request.user.id),
                                        isArchive=False, isTrash=False).distinct()
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
            RedisCrud().put(note_id, serializer.data, request.user.id)
            return Response({"message": "Note Updated Successfully", "status": 200, "data": serializer.data},
                            status=200)
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
            RedisCrud().delete(note_id, request.user)
            return Response({"message": "Note Deleted Successfully", "status": 200, "data": {}},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class LabelsAPIViews(APIView):
    """
            LabelsAPIView : GET, ADD, UPDATE, DELETE Labels
    """
    serializer_class = LabelsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
            return Response({"message": "Label Updated Successfully", "status": 200, "data": serializer.data},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LabelsSerializer, operation_summary='Delete Label')
    def delete(self, request, label_name):
        try:
            labels = Labels.objects.get(label_name=label_name, user=request.user)
            labels.delete()
            return Response({"message": "Label Deleted Successfully", "status": 200, "data": {}},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class TrashNotesAPIView(APIView):
    """
          TrashNotesAPIView: Trash notes And Restore notes.
    """
    serializer_class = NotesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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


class NotesCollaboratorAPIViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, properties={
            'collaborator': openapi.Schema(type=openapi.TYPE_ARRAY,
                                           items=openapi.Items(type=openapi.TYPE_STRING))}),
        responses={201: "ok", 400: "BAD REQUEST"})
    def post(self, request, id):
        try:
            note = Note.objects.get(id=id, user=request.user.id)
            collab_list = request.data.get('collaborator')
            for user_name in collab_list:
                c_user = User.objects.get(username=user_name)
                if request.user != c_user:
                    note.collaborator.add(c_user)
            return Response({"Message": "Collaborator Added Successfully", 'status': 200})
        except Exception as e:
            logger.exception(e)
            return Response({"Message": str(e)}, status=400)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, properties={
            'collaborator': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))}),
        responses={201: "ok", 400: "BAD REQUEST"})
    def delete(self, request, id):

        try:
            note = Note.objects.get(id=id, user=request.user.id)
            collab_list = request.data.get('collaborator')
            for user_name in collab_list:
                user = User.objects.get(username=user_name)
                if request.user != user:
                    note.collaborator.remove(user)
            return Response({"Message": "Collaborator Deleted Successfully", 'status': 200})
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e)}, status=400)
