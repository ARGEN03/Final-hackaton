from django.contrib import admin
from .models import Favorite
# Register your models here.

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('movie', 'owner_email')  
    search_fields = ['movie__title']
    # list_filter = ('title', 'director', 'release_at',)
    readonly_fields = ('owner',)  

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def owner_email(self, obj):
        return obj.owner.email if obj.owner else ''  
    owner_email.short_description = 'Owner'  

admin.site.register(Favorite, FavoriteAdmin)