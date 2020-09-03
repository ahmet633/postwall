from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.conf import settings
from posts.models import Post
from posts.serializers import PostSerializer

User = settings.AUTH_USER_MODEL

################ authentication views #############################
def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("/")
    context = {
        "form" : form,
        "btn_label": "Login",
        "title": "LOGIN",
    }
    return render(request, "accounts/login.html", context)

def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    context = {
        "form": None,
        "btn_label": "Logout?",
        "title": "LOGOUT",
    }
    return render(request, "accounts/logout.html", context)

def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.get_cleaned_data().get("password1"))
        login(request, user)
        return redirect("/")
    return render(request, "accounts/register.html", {"form": form})


def change_password_view(request, *args, **kwargs):
    form = PasswordResetForm(request.Post or None)
    return render(request, "accounts/profile.html", {"form": form})


################ profile views #############################
def profile_view(request, username, *args, **kwargs):
    form = PasswordChangeForm(request.GET or None)
    context = {
        "username": username,
        "form": form,
    }
    return render(request, "accounts/profile.html", context)

def get_posts_user(request, user, *args, **kwargs):
    qs = Post.objects.filter(user=user)
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)
