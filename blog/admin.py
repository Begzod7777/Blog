from django.contrib import admin
from .models import Article, Comment, Category, Advertisement

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

admin.site.register(Advertisement, AdvertisementAdmin)  # Faqat bitta marta ro‘yxatdan o‘tkazamiz!
