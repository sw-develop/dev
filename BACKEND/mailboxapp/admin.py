from django.contrib import admin

from .models import MailBox


class DateAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'last_updated', )


admin.site.register(MailBox, DateAdmin)
