from django.contrib import admin
from .models import Favorite
# Register your models here.

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('movie', 'owner_email')  # Отображение имени пользователя владельца
    search_fields = ['movie__title']
    # list_filter = ('title', 'director', 'release_at',)
    readonly_fields = ('owner',)  # Добавляем это поле в readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def owner_email(self, obj):
        return obj.owner.email if obj.owner else ''  # Возвращаем имя владельца, если он существует, иначе пустую строку
    owner_email.short_description = 'Owner'  # Определяем отображаемое имя для колонки

admin.site.register(Favorite, FavoriteAdmin)