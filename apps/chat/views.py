import json
from collections.abc import AsyncGenerator
from django.views import View

import psycopg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    StreamingHttpResponse,
)
from django.shortcuts import get_object_or_404, render

from apps.chat.models import ChatMessage, Room
from apps.chat.utils import sse_message, notify
from apps.users.models import Avatar


class IndexView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "rooms": Room.objects.all(),
            "avatars": Avatar.objects.all(),
            "isAvatar": request.user.avatar is not None,
        }
        return render(request, "chat/index.html", context)


class ChatMessageView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        room = get_object_or_404(Room, slug=slug)
        context = {
            "cuurent_room": room,
            "rooms": Room.objects.all(),
            "messages": ChatMessage.objects.filter(room=room).all(),
            "avatars": Avatar.objects.all(),
            "isAvatar": request.user.avatar is not None,
        }
        return render(request, "chat/chat.html", context)

    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        room = get_object_or_404(Room, slug=slug)
        message = request.POST.get("message")
        if not message:
            return HttpResponseBadRequest("No message provided")
        message = ChatMessage.objects.create(user=request.user, room=room, text=message)
        notify(
            channel="lobby",
            event="message_created",
            event_id=message.id,
            data=message.as_json(),
        )
        return HttpResponse("OK")


async def stream_messages(last_id: int | None = None) -> AsyncGenerator[str, None]:
    connection_params = connection.get_connection_params()

    # Remove the cursor_factory parameter since I can't get
    # the default from Django 4.2.1 to work.
    # Django 4.2 didn't have the parameter and that worked.
    connection_params.pop("cursor_factory")

    aconnection = await psycopg.AsyncConnection.connect(
        **connection_params,
        autocommit=True,
    )
    channel_name = "lobby"

    # Uncomment the following to generate random message to
    # test that we are streaming messages that are created
    # while the client is disconnected.

    # await ChatMessage.objects.acreate(
    #     user="system",
    #     text="randomly generated", room=channel_name)

    if last_id:
        messages = ChatMessage.objects.filter(id__gt=last_id)
        async for message in messages:
            yield sse_message(
                event="message_created",
                event_id=message.id,
                data=message.as_json(),
            )

    async with aconnection.cursor() as acursor:
        await acursor.execute(f"LISTEN {channel_name}")
        gen = aconnection.notifies()
        async for notify_message in gen:
            payload = json.loads(notify_message.payload)
            event = payload.get("event")
            event_id = payload.get("event_id")
            data = payload.get("data")
            yield sse_message(
                event=event,
                event_id=event_id,
                data=data,
            )


async def stream_messages_view(request: HttpRequest) -> StreamingHttpResponse:
    last_id = request.headers.get("Last-Event-ID")
    return StreamingHttpResponse(
        streaming_content=stream_messages(last_id=last_id),
        content_type="text/event-stream",
    )
