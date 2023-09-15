from django.urls import path

from apps.users import views


app_name = "users"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("update-avatar/", views.UpdateAvatarView.as_view(), name="update_avatar"),
]
