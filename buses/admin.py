from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import Sum
from datetime import date
from .models import *
from internal.models import *

all1zed_commission = float(All1zedBusCommission.objects.all().first().commission_per_ticket)


class BusIMageInline(admin.StackedInline):
    model = BusImage


class BusCompanyImageInline(admin.StackedInline):
    model = BusCompanyImage


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        Allowing Bus HQ admins to only access only those buses that were belong to them.
        """
        qs = super(BusAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Bus HQ').exists:
            return qs.filter(bus_company__user=request.user)
        elif request.user.groups.filter(name='Bus Operator').exists:
            return qs.filter(bus_admin=request.user)
    list_display = [
        'bus_full_name', 'total_seats', 'total_tickets_sold', 'sold_on_station', 'sold_by_all1zed',
        'total_all1zed_sales', 'your_earnings', 'all1zed_earnings',

    ]
    inlines = [BusIMageInline]

    def total_tickets_sold(self, bus: Bus):
        return Ticket.objects.filter(bus=bus, departure_date=date.today()).count()

    def total_seats(self, bus: Bus):
        return bus.number_of_seats

    def sold_on_station(self, bus: Bus):
        return 0

    def sold_by_all1zed(self, bus: Bus):
        return Ticket.objects.filter(bus=bus, departure_date=date.today()).count()

    def total_all1zed_sales(self, bus):
        if Ticket.objects.filter(bus=bus, departure_date=date.today()).aggregate(Sum('price'))['price__sum'] is None:
            return f"K{0}"
        else:
            return f"K{float(Ticket.objects.filter(bus=bus, departure_date=date.today()).aggregate(Sum('price'))['price__sum'])}"

    def your_earnings(self, bus: Bus):
        total_tickets_sold = Ticket.objects.filter(bus=bus, departure_date=date.today()).count()
        total_earnings = Ticket.objects.filter(bus=bus, departure_date=date.today()).aggregate(Sum('price'))['price__sum']
        if total_earnings is not None:
            return f'K{float(total_earnings) - (all1zed_commission * total_tickets_sold)}'
        else:
            return 0

    def all1zed_earnings(self, bus):
        total_tickets_sold = Ticket.objects.filter(bus=bus, departure_date=date.today()).count()
        total = Ticket.objects.filter(bus=bus, departure_date=date.today()).aggregate(Sum('price'))['price__sum']
        if total is not None:
            return f'K{(all1zed_commission * float(total_tickets_sold))}'
        else:
            return 0


@admin.register(BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'company_phone_number', 'company_email'
    ]
    inlines = [BusCompanyImageInline, ]


class TicketAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        Allowing Bus HQ admins to only access only those buses that were belong to them.
        """
        qs = super(TicketAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Bus HQ').exists:
            return qs.filter(bus__bus_company__user=request.user)
        elif request.user.groups.filter(name='Bus Operator').exists:
            return qs.filter(bus__bus_admin=request.user)
    list_display = [
        'ticket_number', 'passenger_first_name', 'passenger_last_name', 'date_bought', 'departure_date',
        'scanned',
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
admin.site.register(BusCompanyImage)
