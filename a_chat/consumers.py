from channels.generic.websocket import WebsocketConsumer
import json
from asyncio import sleep
from random import randint
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string

from .models import Chat, ChatMessage


class WSconsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_group_name = self.scope["url_route"]["kwargs"]["chat_id"]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        user = self.scope["user"]

        text_data_json = json.loads(text_data)
        text = text_data_json["text"]

        chat = Chat.objects.get(id=self.room_group_name)
        message = ChatMessage.objects.create(sender=user, body=text, group=chat)
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message_id": message.id}
        )

    def chat_message(self, event):
        message_id = event["message_id"]
        message = ChatMessage.objects.get(id=message_id)
        html = render_to_string(
            "a_chat/partial_message_detail.html",
            {"message": message, "user": self.scope["user"]},
        )
        self.send(text_data=json.dumps({"type": "chat", "html": html}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
