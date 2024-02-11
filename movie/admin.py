from django.contrib import admin
from .models import Movie

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner_email')  # Отображение имени пользователя владельца
    search_fields = ('title', 'director', 'release_at', 'genre_slug')
    list_filter = ('title', 'director', 'release_at','genre')
    readonly_fields = ('owner',)  # Добавляем это поле в readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def owner_email(self, obj):
        return obj.owner.email if obj.owner else ''  # Возвращаем имя владельца, если он существует, иначе пустую строку
    owner_email.short_description = 'Owner'  # Определяем отображаемое имя для колонки

admin.site.register(Movie, MovieAdmin)



