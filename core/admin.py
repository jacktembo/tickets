from django.contrib import admin
from .models import KazangSession


@admin.register(KazangSession)
class KazangSessionAdmin(admin.ModelAdmin):
    list_display = ['session_uuid', 'date_time_created']
