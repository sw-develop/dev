from django.contrib import admin

from .models import Letter


class DateAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'last_updated', )


admin.site.register(Letter, DateAdmin)
