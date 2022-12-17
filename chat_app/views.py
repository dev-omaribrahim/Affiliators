from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from users.models import Marketer

from .models import Chat, Message


def msg_page(request):
    if request.user.is_superuser or request.user.is_staff:
        support_chats = Chat.objects.filter(chat_support=request.user)
        context = {"support_chats": support_chats}
        return render(request, "chat_app/msg_page_for_supporter.html", context)
    else:
        try:
            marketer = Marketer.objects.get(username=request.user.username)
            marketer_chat = Chat.objects.get(chat_marketer=marketer)
        except ObjectDoesNotExist:
            marketer_chat = None

        context = {"marketer_chat": marketer_chat}
        return render(request, "chat_app/msg_page_for_marketer.html", context)


def send_msg(request):
    pass
