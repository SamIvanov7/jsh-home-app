from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test


def handler500(request):
    return render(request, "500.html", status=500)


def handler403(request, exception):
    return render(request, "403.html", status=403)


def handler404(request, exception):
    return render(request, "404.html", status=404)


# User's profession check decorators
def elektriker_check(user):
    return User.objects.filter(id=user.id, beruf="Elektriker").exists()


def verkaufer_check(user):
    return User.objects.filter(id=user.id, beruf="Vertrieb").exists()


class ElektrikerCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return elektriker_check(self.request.user)  # type: ignore


class LoginView(APIView):
    def get(self, request):
        return render(request, "pages-login.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_staff == True:  # type: ignore
            login(request, user)
            return redirect("/admin")
        if user is not None and user.beruf == "Elektriker":  # type: ignore
            login(request, user)
            return redirect("invoices:home")
        elif user is not None and user.beruf == "Vertrieb":  # type: ignore
            login(request, user)
            return redirect("vertrieb_interface:home")
        else:
            return render(request, "pages-login.html", {"error": "Invalid credentials"})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, "logout.html", {"message": "Logout successful"})

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("authentication:logout")
