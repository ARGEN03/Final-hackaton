from django.db import models
from django.contrib.auth import get_user_model
from genre.models import Genre


# Create your models here.
User = get_user_model()

class Movie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie')
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, related_name='movie', null=True)  # Указываем поле для связи
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    director = models.CharField(max_length=150, null=True)
    release_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильм'