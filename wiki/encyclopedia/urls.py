from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Random", views.getRandom, name="random"),
    path("search", views.search, name="search"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>", views.wikipage, name="wikipage"),
]
