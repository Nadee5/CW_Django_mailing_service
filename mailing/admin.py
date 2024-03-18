from django.contrib import admin

from mailing.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'comment',)
    list_filter = ('email', 'comment')
    search_fields = ('first_name', 'last_name', 'email', 'comment',)
