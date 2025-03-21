from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')  # Admin panelda ko‘rinadigan ustunlar
    search_fields = ('title',)  # Qidirish maydoni
    list_filter = ('created_at',)  # Filtrlash imkoniyati

admin.site.register(Post, PostAdmin)