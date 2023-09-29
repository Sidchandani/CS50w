from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("create", views.create, name="create"),
    path("close_view/<int:id>", views.close_view, name="close_view"),
    path("post_comm/<int:id>", views.post_comm, name="post_comm"),
    path("quick_view/<int:id>", views.quick_view, name="quick_view"),
    path("categories", views.categories, name="categories"),
    path("show_cat<str:cat>", views.show_cat, name="show_cat"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
