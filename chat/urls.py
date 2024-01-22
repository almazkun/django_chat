from django.urls import path

from chat.views import ChatListView, ChatView, MyLoginView, MyLogoutView, SignUpView

urlpatterns = [
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/logout/", MyLogoutView.as_view(), name="logout"),
    path("chat/<str:pk>/", ChatView.as_view(), name="chat"),
    path("", ChatListView.as_view(), name="chat_list"),
]
