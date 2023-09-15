from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View

from apps.users.models import Avatar


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("chat:index")
        return render(request, "auth/login.html")


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        logout(request)
        return redirect("chat:index")


class UpdateAvatarView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        avatar_id = int(request.POST.get("avatar"))
        avatar = Avatar.objects.get(pk=avatar_id)
        request.user.avatar = avatar
        request.user.save()
        return redirect("chat:index")
