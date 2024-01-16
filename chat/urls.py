from django.urls import path
from django.contrib.auth import views as auth_views

from chat.views import ChatRoomListView, ChatRoomView

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("chat/<str:pk>/", ChatRoomView.as_view(), name="chat"),
    path("", ChatRoomListView.as_view(), name="chat_list"),
]
