from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

from .models import Movie

User = get_user_model()

@shared_task
def send_email_to_all_users_about_new_movie(movie_id):
    movie = Movie.objects.get(id=movie_id)
    email_list = User.objects.filter(is_superuser=False).values_list('email', flat=True)
    
    subject = f"Новый фильм добавлен для просмотра на нашем сайте: {movie.title}"
    from_email = settings.EMAIL_HOST_USER

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{movie.title}</title>
    </head>
    <body>
        <h1>{movie.title}</h1>
        <p>{movie.content}</p>
        <p>Режиссёр: {movie.director}</p>
        '<p>Смотреть фильм: http://34.125.237.140/media/{movie.video}</p>' 
    </body>
    </html>
    """
    
    if email_list:
        email = EmailMessage(
            subject,
            html_content,
            from_email,
            bcc = list(email_list),
        )
        email.content_subtype = "html"
        email.send()