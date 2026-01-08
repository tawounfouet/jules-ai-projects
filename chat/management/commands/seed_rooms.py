from django.core.management.base import BaseCommand
from django.utils.text import slugify
from chat.models import Room

class Command(BaseCommand):
    help = 'Seeds the database with default public rooms'

    def handle(self, *args, **options):
        rooms = ["Général", "Random", "Dev Team"]
        for name in rooms:
            slug = slugify(name)
            room, created = Room.objects.get_or_create(slug=slug, defaults={'name': name})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created room: {name}"))
            else:
                self.stdout.write(f"Room already exists: {name}")
