from django.contrib import admin

from apps.chat.models import ChatMessage, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "icon"]
    list_editable = ["icon"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["user", "text", "room", "created"]
    list_editable = ["text", "room"]
