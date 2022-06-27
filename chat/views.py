# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


@login_required
def index(request):
    user = get_user_model()
    all_users = user.objects.all()
    return render(request, 'chat/index.html', {'all_user': all_users})


@login_required
def room(request, room_name):
    return render(request, 'chat/chat.html', {
        'room_name': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username))
    })

