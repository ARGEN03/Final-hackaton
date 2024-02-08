from django.db import models
from django.contrib.auth import get_user_model
from movie.models import Movie

User = get_user_model()

# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateField(auto_now_add=True)
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментраий'
        verbose_name_plural = 'Комментраии'

class Like(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='likes'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

