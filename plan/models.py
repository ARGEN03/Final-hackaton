from django.db import models
from django.contrib.auth import get_user_model
from movie.models import Movie

User = get_user_model()

# Create your models here.

class Plan(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='plans')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'movie']
        verbose_name = 'Планы'
        verbose_name_plural = 'Планы'