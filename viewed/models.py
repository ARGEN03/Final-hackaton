from django.db import models
from django.contrib.auth import get_user_model
from movie.models import Movie

User = get_user_model()

# Create your models here.

class Viewed(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'movie']