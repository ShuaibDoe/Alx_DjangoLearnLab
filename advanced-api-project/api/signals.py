from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Book)
def log_new_book(sender, instance, created, **kwargs):
    if created:
        logger.info(f"📚 New book added: {instance.title} by {instance.author}")
        # Simulate background task (e.g., send email, call API)
        simulate_background_task(instance)

def simulate_background_task(book):
    """
    Simulate a background process. 
    In production, you'd trigger Celery/RQ here.
    """
    print(f"[Background Task] Processing notifications for book '{book.title}'...")
