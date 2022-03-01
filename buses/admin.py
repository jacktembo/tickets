from django.contrib.auth.models import User
from django.contrib import admin
from .models import *


class BusIMageInline(admin.StackedInline):
    model = BusImage


class BusCompanyImageInline(admin.StackedInline):
    model = BusCompanyImage


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_company', 'bus_full_name', 'number_of_seats',]
    inlines = [BusIMageInline]


@admin.register(BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'company_phone_number', 'company_email'
    ]
    inlines = [BusCompanyImageInline, ]

admin.site.register(Route)