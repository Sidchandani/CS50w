from django.urls import path

from . import views

# no need of app name becz this proj conatins only single app
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show, name="show"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random")
]
