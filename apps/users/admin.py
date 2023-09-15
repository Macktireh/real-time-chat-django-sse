from typing import cast

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import (
    GroupAdmin as BaseGroupAdmin,
    UserAdmin as BaseUserAdmin,
)
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.users.models import Avatar, GroupProxy, User


admin.site.unregister(Group)


@admin.register(GroupProxy)
class GroupAdmin(BaseGroupAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "name",
        "avatar",
        "avatar_preview",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    list_filter = (
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_editable = ("avatar",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "publicId",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "avatar_preview",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    readonly_fields = (
        "date_joined",
        "last_login",
        "avatar_preview",
        "publicId",
    )
    search_fields = (
        "email",
        "name",
    )
    ordering = ("date_joined",)
    list_per_page = 20

    def has_view_permission(
        self, request: HttpRequest, obj: User | None = None
    ) -> bool:
        return cast(User, request.user).is_superuser

    def has_add_permission(self, request: HttpRequest) -> bool:
        return cast(User, request.user).is_superuser

    def has_change_permission(
        self, request: HttpRequest, obj: User | None = None
    ) -> bool:
        return cast(User, request.user).is_superuser

    def has_delete_permission(
        self, request: HttpRequest, obj: User | None = None
    ) -> bool:
        return cast(User, request.user).is_superuser


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "avatar_preview",
    )
