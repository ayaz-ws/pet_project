from django.urls import path
from .consumers import WSconsumer

websocket_urlpatterns = [
    path("ws/<chat_id>/", WSconsumer.as_asgi()),
]
