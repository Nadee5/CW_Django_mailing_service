from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'views_count', 'publication_date',)
    list_filter = ('title', 'views_count', 'publication_date',)
    search_fields = ('title', 'content', 'publication_date',)
