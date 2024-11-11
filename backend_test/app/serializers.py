from rest_framework import serializers
from app.models import Book, Author


class AuthorSerioulizer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "date_of_birth",
        ]


class BookSerioulizer(serializers.ModelSerializer):
    author = AuthorSerioulizer(many=False)

    class Meta:
        model = Book
        fields = ["id", "title", "published_date", "genre", "is_archived", "author"]
        read_only_fields = ["is_archived"]

    def create(self, validated_data):
        author_data = validated_data.pop("author")
        author = Author.objects.create(**author_data)
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop("author")
        author = instance.author
        author.name = author_data.get("name", author.name)
        author.date_of_birth = author_data.get("date_of_birth", author.date_of_birth)
        author.save()
        instance.title = validated_data.get("title", instance.title)
        instance.published_date = validated_data.get(
            "published_date", instance.published_date
        )
        instance.genre = validated_data.get("genre", instance.genre)
        instance.save()
        return instance
