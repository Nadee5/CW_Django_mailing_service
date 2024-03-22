from django.contrib import admin

from mailing.models import Client, Mailing, Message, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'comment',)
    list_filter = ('email', 'comment')
    search_fields = ('first_name', 'last_name', 'email', 'comment',)


admin.site.register(Mailing)

admin.site.register(Message)

admin.site.register(Logs)