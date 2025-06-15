from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name="chats")



class ChatMessage(models.Model):
    group = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.body