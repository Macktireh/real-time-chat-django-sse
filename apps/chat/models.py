import json
from typing import Any, Dict, Tuple

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.template.defaultfilters import slugify

from apps.users.models import User


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    icon = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "rooms"

    def __str__(self) -> str:
        return self.name

    def save(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"

    def __str__(self) -> str:
        if len(self.text) > 10:
            return f"{self.user}: {self.text[:10]}..."
        else:
            return f"{self.user}: {self.text}"

    def as_json(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "slug": self.room.slug,
                "user": self.user.as_json(),
                "text": self.text,
                "created": str(naturaltime(self.created)),
            },
        )
