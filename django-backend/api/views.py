from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import UserSerializer, MessageSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


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


@api_view(['GET'])
def public_health(request):
    """Public health check endpoint (no authentication required)"""
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now(),
        'service': 'pngtomap-api'
    })
