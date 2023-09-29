
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("user/<str:username>", views.user, name="user"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    #API Routes
    path("post", views.post, name="post"),
    path("post/<int:postid>", views.edit, name="edit"),
    path("follow/<str:status>", views.follow, name="follow"),

]
