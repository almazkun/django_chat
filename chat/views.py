from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import Chat
from django.contrib.auth.views import LoginView
from chat.forms import LoginForm, SignUpForm
from django.contrib.auth.views import LogoutView


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "chat/signup.html"
    success_url = "/"


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "chat/login.html"
    success_url = "/"


class MyLogoutView(LoginRequiredMixin, LogoutView):
    def get_success_url(self):
        return "/"


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chat/chat_list.html"
    context_object_name = "chat_list"

    def get_queryset(self):
        return self.request.user.chats.all()


class ChatView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "chat/chat_list.html"
    context_object_name = "chat"

    def get_queryset(self):
        return self.request.user.chats.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat_list"] = self.request.user.chats.all()
        context["message_list"] = self.object.messages.all().select_related("sender")
        return context
