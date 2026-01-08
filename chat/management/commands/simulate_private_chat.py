from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from chat.models import Room, Message
import time

class Command(BaseCommand):
    help = 'Simulates a private chat scenario between two users'

    def handle(self, *args, **options):
        # 1. Create Users
        self.stdout.write("Creating users Alice and Bob...")
        alice, _ = User.objects.get_or_create(username='alice')
        alice.set_password('password123')
        alice.save()
        
        bob, _ = User.objects.get_or_create(username='bob')
        bob.set_password('password123')
        bob.save()

        # 2. Create "Private" Room
        # Convention: Alphabetical order of usernames for unique room ID
        room_name = f"Private: {alice.username} & {bob.username}"
        unique_slug = slugify(f"private-{min(alice.username, bob.username)}-{max(alice.username, bob.username)}")
        
        self.stdout.write(f"Creating hidden private room: {unique_slug}...")
        room, created = Room.objects.get_or_create(
            slug=unique_slug,
            defaults={'name': room_name}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new room: {room.name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Room already exists: {room.name}"))

        # 3. Simulate Conversation
        self.stdout.write("Simulating message exchange...")
        
        messages_data = [
            (alice, "Salut Bob ! Tu as vu le match ?"),
            (bob, "Salut Alice ! Oui, incroyable ce but à la fin."),
            (alice, "Grave, je ne m'y attendais pas."),
            (bob, "On se voit demain pour en parler ?"),
            (alice, "Ça marche, à demain !")
        ]

        for user, content in messages_data:
            msg = Message.objects.create(room=room, user=user, content=content)
            self.stdout.write(f"[{msg.timestamp.strftime('%H:%M:%S')}] {user.username}: {content}")
            # emulate slight delay if we were watching it live, but instant for db population is fine
        
        self.stdout.write(self.style.SUCCESS(f"Successfully simulated conversation in room '{room.slug}'"))
