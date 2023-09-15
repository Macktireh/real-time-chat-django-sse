from django.urls import path

from apps.chat import views


app_name = "chat"


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("room/<str:slug>/", views.ChatMessageView.as_view(), name="room"),
    path("messages/", views.stream_messages_view, name="stream-messages"),
]
