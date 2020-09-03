"""tempuswall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from posts.views import home_view, post_details, post_list_view, post_create_view, post_delete_view, post_like_view
from accounts.views import login_view, register_view, logout_view, profile_view, get_posts_user

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),

    # tempuspost api urls
    path('api/post/<int:post_id>', post_details),
    path('api/posts/', post_list_view),
    path('api/post/create', post_create_view),
    path('api/post/<int:post_id>/delete', post_delete_view),
    path('api/post/<int:post_id>/like', post_like_view),

    # auth urls
    path('login/', login_view),
    path('register/', register_view),
    path('logout/', logout_view),

    # profile url
    path('profile/<str:username>/', profile_view),
    path('api/profile/<str:username>/posts', get_posts_user),
]
