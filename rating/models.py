from django.db import models
from movie.models import Movie
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

class Rating(models.Model):
    RATING_CHOICES = (
        (1,'Too bad'),
        (2,'bad'),
        (3,'Normal'),
        (4,'Good'),
        (5,'Perfect')
    )

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    
    class Meta:
        unique_together = ['owner','movie']
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        