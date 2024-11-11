from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.models import Book


@receiver(post_save, sender=Book)
def book_post_save(sender, instance, created, **kwargs):
    print(f"Book {instance.title} has been saved")


@receiver(post_delete, sender=Book)
def book_post_delete(sender, instance, **kwargs):
    print(f"Book {instance.title} has been deleted")
