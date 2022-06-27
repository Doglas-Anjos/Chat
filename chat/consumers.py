# chat/consumers.py
import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        room_name = data['room_name']
        print(room_name)
        messages = Message.last_30_messages(room_name)
        content = content = {
            'command': 'fetch_messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        return [self.message_to_json(i) for i in messages]

    def message_to_json(self, message):
        return {
            'author': message.user.username,
            'author_pk': message.user.pk,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%d/%m/%Y %H:%M')
        }

    def new_message(self, data):
        author_pk = data['from']
        room_name = data['room_name']
        room = RoomUser.return_room_user(room_name)
        author_user = User.objects.get(pk=author_pk)
        message = Message.objects.create(
            user=author_user,
            room=room,
            content=data['message']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        "fetch_messages": fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print('recebeu')
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(message)
    # Receive message from room group

    def chat_message(self, event):
        message = event['message']
        print(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))