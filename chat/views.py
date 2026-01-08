from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, "chat/index.html", {"rooms": rooms})

@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = room.messages.all()
    return render(request, "chat/room.html", {"room": room, "messages": messages})
