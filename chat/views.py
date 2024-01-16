from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chat/chat_list.html"
    context_object_name = "chat_list"

    def get_queryset(self):
        return self.request.user.chat_rooms.all()


class ChatRoomView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "chat/chat_list.html"
    context_object_name = "message_list"

    def get_queryset(self):
        return self.model.objects.filter(chat=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = Chat.objects.get(pk=self.kwargs.get("pk"))
        context["chat_list"] = self.request.user.chat_rooms.all()
        return context
