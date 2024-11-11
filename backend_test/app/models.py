from django.db import models
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=250)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)
    published_date = models.DateField()
    genre = models.CharField(max_length=250)
    is_archived = models.BooleanField(default=False)  # for background task
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="Books")

    def __str__(self):
        return self.title
