from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import UserSerializer, ProjectSerializer
from .models import Project  # Assuming a Project model exists
from rest_framework.decorators import action
from http import HTTPMethod
from django.conf import settings
import os
from django.http import HttpResponse
from basefunc import tasks

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(ModelViewSet):
    # Placeholder for Project model and serializer
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]


    @action(detail=True, methods=[HTTPMethod.POST, HTTPMethod.GET])
    def get_image(self, request, pk=None):
        project = self.get_object()
        # Assuming the Project model has an 'image' field
        if hasattr(project, 'image') and project.image:
            image_url = os.path.join(settings.BASE_DIR, project.image.url.lstrip('/'))
            print(image_url)
            with open(image_url, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        else:
            return Response({'error': 'No image found for this project'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=[HTTPMethod.POST])
    def start_render(self, request, pk=None):
        project = self.get_object()
        if project.status == 'draft':
            project.status = 'pending'
            project.save()
            tasks.render_project.delay(project.id)

            return Response({'status': 'render started'})
        else:
            return Response({'error': f'Cannot start render, current status is {project.status}', 'detail': 'Project is not in draft status'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check(request):
    """Simple health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now(),
        'user': request.user.username
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_websocket_message(request):
    """Send a message to a WebSocket room"""
    room_name = request.data.get('room_name')
    message = request.data.get('message')
    
    if not room_name or not message:
        return Response(
            {'error': 'room_name and message are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    channel_layer = get_channel_layer()
    room_group_name = f'api_{room_name}'
    
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'api_message',
            'message': message,
            'message_type': 'broadcast',
            'user': request.user.username,
            'timestamp': timezone.now().isoformat()
        }
    )
    
    return Response({'status': 'message sent'})
