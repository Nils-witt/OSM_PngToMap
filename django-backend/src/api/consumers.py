import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ApiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'api_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        message_type = text_data_json.get('type', 'message')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'api_message',
                'message': message,
                'message_type': message_type
            }
        )

    # Receive message from room group
    async def api_message(self, event):
        message = event['message']
        message_type = event['message_type']
        user = event.get('user', 'Anonymous')
        timestamp = event.get('timestamp', '')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'type': message_type,
            'user': user,
            'timestamp': timestamp
        }))