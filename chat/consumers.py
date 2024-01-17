from chat.models import Chat, Message
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()

        if not self.user.is_authenticated:
            await self.close()

        if not self.user.is_active:
            await self.close()

        if not await database_sync_to_async(
            Chat.objects.filter(pk=self.chat_pk, users__in=[self.user]).exists
        )():
            await self.close()

        self.group_name = self.chat_pk

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(
            self.group_name,
            {
                "message": f"{self.user.username} has joined the chat",
                "type": "system_notification",
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "message": f"{self.user.username} has left the chat",
                "type": "system_notification",
            },
        )

    async def receive_json(self, content, **kwargs):
        msg = await Message.objects.acreate(
            sender=self.user, text=content["message"], chat_id=self.chat_pk
        )
        await self.channel_layer.group_send(
            self.group_name,
            {
                "sender": msg.sender.username,
                "message": msg.text,
                "type": "chat_message",
            },
        )

    async def chat_message(self, event):
        await self.send_json({"message": event["message"], "sender": event["sender"]})

    async def system_notification(self, event):
        await self.send_json({"message": event["message"], "sender": "system"})
