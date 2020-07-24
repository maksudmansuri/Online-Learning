from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from accounts.models import CustomUser

def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    std1=CustomUser.objects.get(id=request.user.id)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'std1':std1
    })