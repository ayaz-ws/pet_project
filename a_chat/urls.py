from django.urls import path

from .views import chat_view, start_chat, chat_list


urlpatterns = [
    path("start/<int:id>/", start_chat, name="start_chat"),
    path("<int:chat_id>/", chat_view, name="chat"), 
    path("list/", chat_list, name="chat_list"),
    
]