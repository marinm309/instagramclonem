from django.db import models
import uuid
from django.contrib.auth.models import User
from users.models import Profile

class Chat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    other_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

class MainBubble(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500, null=True)
    in_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)


class OtherBubble(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500, null=True)
    in_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)
    other = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)