from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("entry/<str:name>", views.entry, name="entry"),
    path("new_page", views.new_page, name="new_page"),
    path("random", views.random_entry, name="random"),
    path("search", views.search, name="search")
]
