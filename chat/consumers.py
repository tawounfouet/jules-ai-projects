import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = 'chat_%s' % self.room_slug

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

        if 'message' in text_data_json:
            message = text_data_json['message']
            username = self.scope['user'].username

            # Save message to DB
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
        elif 'typing' in text_data_json:
             typing = text_data_json['typing']
             username = self.scope['user'].username

             await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'typing': typing,
                    'username': username
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def user_typing(self, event):
        typing = event['typing']
        username = event['username']

        await self.send(text_data=json.dumps({
            'typing': typing,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, room_slug, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_slug)
        Message.objects.create(user=user, room=room, content=message)
