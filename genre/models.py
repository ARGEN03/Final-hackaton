from autoslug import AutoSlugField
from django.db import models

# Create your models here.
# class Genre(models.Model):
#     name = models.CharField(max_length=60, unique=True)
#     parent = models.ForeignKey(
#         'self',
#         on_delete = models.SET_NULL,
#         null=True, blank=True,
#         related_name = 'children'       
#         )
#     slug = AutoSlugField(populate_from='name', always_update=True)
    
#     def __str__(self) -> str:
#         return self.name

class Genre(models.Model):
    GENRE_CHOICES = (
        ('action', 'Боевик'),
        ('western', 'Вестерн'),
        ('detective', 'Детектив'),
        ('drama', 'Драма'),
        ('historical', 'Исторический фильм'),
        ('comedy', 'Комедия'),
        ('musical', 'Музыкальный фильм'),
        ('adventure', 'Приключенческий фильм'),
        ('fairy_tale', 'Сказка'),
        ('tragedy', 'Трагедия'),
        ('thriller', 'Триллер'),
        ('fantasy', 'Фантастический фильм'),
        ('horror', 'Фильм ужасов'),
        ('disaster', 'Фильм-катастрофа'),
    )
    
    slug = models.SlugField(max_length=50,blank=True, primary_key=True, unique=True)
    title = models.CharField(max_length=50, choices=GENRE_CHOICES)
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

