from django.contrib.auth.models import User
from django.contrib import admin
from .models import *


class BusIMageInline(admin.StackedInline):
    model = BusImage


class BusCompanyImageInline(admin.StackedInline):
    model = BusCompanyImage


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.bus_admin = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Allowing Events admins to only access only those events that were created by them.
        """
        qs = super(BusAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(bus_admin=request.user)

    search_fields = ['bus_company', 'bus_short_name', ]
    list_filter = ['bus_company']
    list_display = ['bus_company', 'bus_full_name', 'number_of_seats', 'mobile_money_number', ]
    inlines = [BusIMageInline]


@admin.register(BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'company_phone_number', 'company_email'
    ]
    inlines = [BusCompanyImageInline, ]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_number', 'passenger_first_name', 'passenger_last_name', 'date_bought'
    ]
    search_fields = ['passenger_first_name']
    list_per_page = 5


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    def departure_time(self, route: Route):
        return route.time.strftime('%H:%M hrs')

    list_display = [
        'bus', 'starting_place', 'destination', 'departure_time', 'price'
    ]


