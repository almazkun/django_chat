from django.contrib.auth.models import AbstractUser, UserManager
import uuid
from django.db import models


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Chat(BaseModel):
    name = models.CharField("Name", max_length=255)
    chat_id = models.CharField("Chat ID", max_length=255)
    users = models.ManyToManyField(CustomUser, related_name="chat_rooms")

    def __str__(self):
        return self.name


class Message(BaseModel):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="messages"
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()

    def __str__(self):
        return self.text[:20] + "..."

    class Meta:
        ordering = ["created_at"]
