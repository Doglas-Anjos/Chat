from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
user = get_user_model()


class RoomUser(models.Model):
    room_name = models.CharField(unique=True, max_length=255)

    @staticmethod
    def return_room_user(room_name):
        r = RoomUser.objects.filter(room_name=room_name)
        if r.exists():
            return r[0]
        else:
            r = RoomUser(room_name=room_name)
            r.save()
            return r


class Message(models.Model):
    room = models.ForeignKey(RoomUser, on_delete=models.CASCADE)
    user = models.ForeignKey(user, related_name='auth', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

    @staticmethod
    def last_30_messages(room_name):
        return Message.objects.filter(room__room_name=room_name).order_by('-timestamp')[:30]