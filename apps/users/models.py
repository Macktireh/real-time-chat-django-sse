import json
from typing import Any, Dict
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.users.managers import UserManager


class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class Avatar(models.Model):
    url = models.CharField(max_length=500)

    class Meta:
        db_table = "avatars"

    def __str__(self) -> str:
        return self.url

    @property
    def avatar_preview(self) -> Any:
        if self.url:
            return mark_safe(
                f'<img src="{self.url}" width="40" height="40" style="border-radius: 50%;" />'
            )
        return "No avatar"


class User(AbstractUser):
    username = None
    publicId = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        _("email address"), max_length=255, unique=True, db_index=True
    )
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.name

    def save(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if not self.publicId:
            self.publicId = str(uuid4())
        super().save(*args, **kwargs)

    @property
    def name(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def avatar_preview(self) -> Any:
        if self.avatar:
            return mark_safe(
                f'<img src="{self.avatar.url}" width="40" height="40" style="border-radius: 50%;" />'
            )
        return ""

    def as_json(self) -> str:
        return json.dumps(
            {
                "publicId": self.publicId,
                "name": self.name,
                "email": self.email,
                "avatar": self.avatar.url,
            },
        )
