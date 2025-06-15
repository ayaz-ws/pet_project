from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Chat, ChatMessage
from .forms import MessageCreateForm


@login_required
def chat_list(request):
    user = request.user
    chats = user.chats.all()

    paginator = Paginator(chats, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "a_chat/chat_list.html", {
        "user": user,
        "page_obj": page_obj,
    })


@login_required
def start_chat(request, id):
    if request.user.id == id:
        return redirect("home")

    other_user = get_object_or_404(User, id=id)

    possible_chats = Chat.objects.filter(members=request.user).filter(
        members=other_user
    )

    for chat in possible_chats:
        members_ids = set(chat.members.values_list("id", flat=True))
        if members_ids == {request.user.id, other_user.id}:
            return redirect("chat", chat_id=chat.id)

    chat = Chat.objects.create()
    chat.members.add(request.user, other_user)
    return redirect("chat", chat_id=chat.id)

@login_required
def chat_view(request, chat_id):

    chat = Chat.objects.get(id=chat_id)
    if not request.user.id in set(chat.members.values_list("id", flat=True)):
        return redirect("home")
    chatname = chat.members.exclude(id=request.user.id).first().username
    messages = chat.messages.all()
    form = MessageCreateForm
   
    return render(
        request,
        "a_chat/chat.html",
        {"chatname": chatname, "form": form, "messages": messages, "chat_id": chat.id},
    )
