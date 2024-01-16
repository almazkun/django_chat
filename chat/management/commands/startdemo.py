from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a demo chat room with some messages."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Creating demo data..."))
        self._create_users()
        self._create_chats()
        self._create_messages()
        self.stdout.write(self.style.SUCCESS("Successfully created demo data."))

    def _create_users(self):
        from chat.models import CustomUser

        self.admin = CustomUser.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin"
        )

        self.user = CustomUser.objects.create_user(
            username="user1", email="user1@example.com", password="user1"
        )

    def _create_chats(self):
        from chat.models import Chat

        chat_name_list = ["My First Chat Room", "My Second Chat Room"]

        self.chat_list = []
        for chat_name in chat_name_list:
            chat = Chat.objects.create(name=chat_name)
            chat.users.add(self.admin, self.user)
            self.chat_list.append(chat)

    def _create_messages(self):
        from chat.models import Message

        message_list = [
            "Hi there!",
            "Nice to meet you!",
            "How are you?",
            "Long time no see!",
            "How is it going?",
            "Not too bad.",
            "What do you do?",
            "I'm a programmer.",
            "What programming languages do you know?",
            "Mainly Python and JavaScript.",
            "That's cool!",
            "Yeah!",
        ]

        for chat in self.chat_list:
            for message in message_list:
                for sender in chat.users.all():
                    Message.objects.create(sender=sender, chat=chat, text=message)
