from django.urls import path
from . import views

urlpatterns = [
    path("list-books/", views.book_query, name="book-query"),
    path("found/", views.book_found, name="book-found"),
    path("not-found/", views.book_not_found, name="book-not-found"),
]
