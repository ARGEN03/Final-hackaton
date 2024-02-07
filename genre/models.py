from autoslug import AutoSlugField
from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = AutoSlugField(populate_from='name', always_update=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"