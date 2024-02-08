from django.contrib import admin
from .models import Genre

# Register your models here.
class Genrechild(admin.ModelAdmin):
    list_display = ['name', 'parent']

admin.site.register(Genre, Genrechild)