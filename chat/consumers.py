import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "the_chat_room"
        self.group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
