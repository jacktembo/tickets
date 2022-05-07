from django.contrib.auth.models import User
from django.contrib import admin
from .models import *


class BusIMageInline(admin.StackedInline):
    model = BusImage


class BusCompanyImageInline(admin.StackedInline):
    model = BusCompanyImage


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_company', 'bus_full_name', 'number_of_seats', ]
    list_filter = ['bus_company']
    inlines = [BusIMageInline]


@admin.register(BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'company_phone_number', 'company_email'
    ]
    inlines = [BusCompanyImageInline, ]


class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_number', 'passenger_first_name', 'passenger_last_name', 'date_bought', 'departure_date'
    ]
    search_fields = ['passenger_first_name', 'ticket_number']
    list_filter = ['date_bought', 'departure_date']
    list_per_page = 7


class RouteAdmin(admin.ModelAdmin):
    list_display = [
        'bus', 'starting_place', 'destination', 'departure_time', 'price'
    ]
    search_fields = ['starting_place', 'destination']

    def departure_time(self, route: Route):
        return route.time


admin.site.register(Route, RouteAdmin)
admin.site.register(Ticket, TicketAdmin)
