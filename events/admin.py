from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Event, EventTicket, All1ZedEventsCommission
from django.db.models import Sum

percentage_commission = 7


class All1ZedEventCommissionAdmin(admin.ModelAdmin):
    list_display = ['percentage_commission']

    def has_add_permission(self, request):
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


class EventAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Allowing Events admins to only access only those events that were created by them.
        """
        qs = super(EventAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    list_display = [
        'name', 'total_tickets_sold', 'vvip_tickets_sold', 'vip_tickets_sold',
        'general_tickets_sold', 'your_earnings', 'all1zed_earnings', 'total_sales',
    ]
    search_fields = ['name', 'description', 'venue', 'additional_information', 'organizer']
    list_filter = ['date_starting', 'age_or_gender_restriction']
    list_per_page = 10
    search_help_text = 'Search Events'

    def total_tickets_sold(self, event):
        return EventTicket.objects.filter(event=event).count()

    def vvip_tickets_sold(self, event):
        return EventTicket.objects.filter(event=event, type='VVIP').count()

    def vip_tickets_sold(self, event):
        return EventTicket.objects.filter(event=event, type='VIP').count()

    def general_tickets_sold(self, event):
        return EventTicket.objects.filter(event=event, type='General').count()

    def total_sales(self, event):
        if EventTicket.objects.filter(event=event).aggregate(Sum('ticket_price'))['ticket_price__sum'] is None:
            return f"K{0}"
        else:
            return f"K{EventTicket.objects.filter(event=event).aggregate(Sum('ticket_price'))['ticket_price__sum']}"

    def your_earnings(self, event):
        total_earnings = EventTicket.objects.filter(event=event).aggregate(Sum('ticket_price'))['ticket_price__sum']
        if total_earnings is not None:
            return f'K{total_earnings - ((percentage_commission / 100) * total_earnings)}'
        else:
            return 0

    def all1zed_earnings(self, event):
        total = EventTicket.objects.filter(event=event).aggregate(Sum('ticket_price'))['ticket_price__sum']
        if total is not None:
            return f'K{(percentage_commission / 100) * total}'
        else:
            return 0


admin.site.register(Event, EventAdmin)
admin.site.register(EventTicket)
admin.site.register(All1ZedEventsCommission, All1ZedEventCommissionAdmin)
