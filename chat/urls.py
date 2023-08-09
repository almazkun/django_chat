from django.urls import path

from chat.views import ChatRoomView

urlpatterns = [
    path("", ChatRoomView.as_view(), name="chat_room"),
]
