import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = f'chat_{self.room_slug}'

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
        message_type = text_data_json.get('type', 'chat_message')
        
        if message_type == 'chat_message':
            message = text_data_json['message']
            username = text_data_json['username'] # Or get from scope["user"]

            # Save message to database
            await self.save_message(username, self.room_slug, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )
        elif message_type == 'typing':
             # Broadcast typing status
             username = text_data_json['username']
             is_typing = text_data_json['is_typing']
             await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'username': username,
                    'is_typing': is_typing
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username
        }))

    # Receive typing event from room group
    async def user_typing(self, event):
        username = event['username']
        is_typing = event['is_typing']

        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': username,
            'is_typing': is_typing
        }))

    @sync_to_async
    def save_message(self, username, room_slug, content):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_slug)
        Message.objects.create(user=user, room=room, content=content)
