from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie
from .tasks import send_email_to_all_users_about_new_movie

@receiver(post_save, sender=Movie)
def movie_post_save(sender, instance, created, **kwargs):
    if created:
        send_email_to_all_users_about_new_movie.delay(instance.id)