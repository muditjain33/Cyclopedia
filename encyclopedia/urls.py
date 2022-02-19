from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("randome", views.randome, name="randome"),
    path("create", views.create , name="create"),
    path("<str:name>", views.page, name="page"),
    path("<str:name>/edit", views.edit, name="edit")
]
