from autoslug import AutoSlugField
from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete = models.SET_NULL,
        null=True, blank=True,
        related_name = 'children'       
        )
    slug = AutoSlugField(populate_from='name', always_update=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

