from django.urls import path
from . import views

urlpatterns = [
    path("list-books/", views.book_query, name="book-query"),
]
