from django.shortcuts import render
from rest_framework import viewsets, filters, status, filters
from app.models import Book, Author
from app.serializers import BookSerioulizer, AuthorSerioulizer
from rest_framework.response import Response
from app.utils import ResponseWrapper
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerioulizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["author_name", "genre", "published_date"]
    search_fields = ["title", "author__name"]

    def get_queryset(self):
        queryset = Book.objects.select_related("author").all().order_by("-id")
        return queryset

    # get list of books
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return ResponseWrapper(data=serializer.data, status=status.HTTP_200_OK)

    # create book
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ResponseWrapper(data=serializer.data, status=status.HTTP_201_CREATED)

    # patch book
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ResponseWrapper(data=serializer.data, status=status.HTTP_200_OK)

    # delete book
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return ResponseWrapper(data={}, status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerioulizer

    def list(self, request, *args, **kwargs):
        queryset = Author.objects.all().order_by("-id")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return ResponseWrapper(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ResponseWrapper(data=serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ResponseWrapper(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return ResponseWrapper(data={}, status=status.HTTP_204_NO_CONTENT)
