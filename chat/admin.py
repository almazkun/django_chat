# Register your models here.
from django.contrib import admin

from chat.models import Chat, CustomUser, Message


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("username", "email")


class ChatAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "chat", "text")
    search_fields = ("sender", "chat", "text")
    ordering = ("-created_at",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
