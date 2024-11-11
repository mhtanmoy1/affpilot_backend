from celery import shared_task
from django.utils import timezone
from app.models import Book


@shared_task
def archive_books():

    ten_years_ago = timezone.now() - timezone.timedelta(days=10 * 365)
    books = Book.objects.filter(published_date__lt=ten_years_ago)
    books.update(is_archived=True)
    return f"{books.count()} books archived"
