from django.test import TestCase
from django.contrib.auth.models import User
from .models import Room, Message

class ChatTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.room = Room.objects.create(name='Test Room', slug='test-room')

    def test_room_creation(self):
        self.assertEqual(self.room.name, 'Test Room')
        self.assertEqual(self.room.slug, 'test-room')

    def test_message_creation(self):
        message = Message.objects.create(user=self.user, room=self.room, content='Hello')
        self.assertEqual(message.content, 'Hello')
        self.assertEqual(message.room, self.room)
        self.assertEqual(message.user, self.user)
