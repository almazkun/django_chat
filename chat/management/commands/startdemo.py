from django.core.management.base import BaseCommand
from django.conf import settings

ADMIN_USERNAME = settings.ADMIN_USERNAME
ADMIN_PASSWORD = settings.ADMIN_PASSWORD


class Command(BaseCommand):
    help = "Create a demo chat with some messages."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Creating demo data..."))
        self._create_users()
        self._create_chat()
        self._create_message()
        self.stdout.write(self.style.SUCCESS("Successfully created demo data."))

    def _create_users(self):
        from django.contrib.auth import get_user_model

        try:
            self.admin = get_user_model().objects.create_superuser(
                username=ADMIN_USERNAME, password=ADMIN_PASSWORD
            )
        except Exception:
            self.admin = get_user_model().objects.get(username=ADMIN_USERNAME)

    def _create_chat(self):
        from chat.models import Chat

        self.chat = Chat.objects.get_or_create(name="Lobby")[0]
        self.chat.users.add(self.admin)

    def _create_message(self):
        from chat.models import Message

        Message.objects.get_or_create(
            sender=self.admin, chat=self.chat, text="Hello from admin"
        )
