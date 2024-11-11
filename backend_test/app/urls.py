from app.models import Book, Author
from app.views import BookViewSet, AuthorViewSet
from django.urls import path

urlpatterns = [
    path(
        "book",
        BookViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="Books",
    ),
    path(
        "book/<int:pk>",
        BookViewSet.as_view(
            {
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="Book",
    ),
    path(
        "author",
        AuthorViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="author",
    ),
    path(
        "author/<int:pk>",
        AuthorViewSet.as_view(
            {
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="author",
    ),
]
