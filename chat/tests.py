from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import path

from chat.models import Chat
from chat.consumers import ChatConsumer


class TestView(TestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }

    def test_signup_login_logout(self):
        endpoint = reverse("signup")
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/signup.html")

        data = self.data.copy()

        response = self.client.post(endpoint, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="testuser").exists())

        endpoint = reverse("login")
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/login.html")

        data = {"username": self.data["username"], "password": "testpassword"}
        response = self.client.post(endpoint, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, "/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "testuser")
        self.assertTrue(response.wsgi_request.user.chats.exists())
        self.assertTrue(response.wsgi_request.user.chats.first().name, "Lobby")

        endpoint = reverse("logout")
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(endpoint)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, "/")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_chat_list(self):
        self.client.post(reverse("signup"), self.data)
        self.client.post(
            reverse("login"),
            {"username": self.data["username"], "password": "testpassword"},
        )

        endpoint = reverse("chat_list")
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chat_list.html")
        self.assertTrue(response.context["chat_list"])
        self.assertEqual(response.context["chat_list"].count(), 1)

        chat = response.context["chat_list"].first()
        self.assertEqual(chat.name, "Lobby")
        self.assertEqual(chat.users.count(), 1)
        self.assertEqual(chat.users.first().username, "testuser")

        endpoint = reverse("chat", kwargs={"pk": chat.pk})
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chat_list.html")
        self.assertTrue(response.context["chat"])
        self.assertEqual(response.context["chat"].name, "Lobby")
        self.assertFalse(response.context["message_list"])


class TestWebsocket(TestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.user = get_user_model().objects.create_user(
            username=self.data["username"], password=self.data["password1"]
        )

        self.chat = Chat.objects.create(name="Lobby")
        self.chat.users.add(self.user)

    async def test_ws(self):
        application = URLRouter(
            [
                path("/ws/chat/<chat_pk>/", ChatConsumer.as_asgi()),
            ]
        )
        communicator = WebsocketCommunicator(application, f"/ws/chat/{self.chat.pk}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
