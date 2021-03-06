from django.contrib import admin
from .models import TermsAndConditions, All1zedBusCommission, Transaction


@admin.register(All1zedBusCommission)
class All1ZedEventCommissionAdmin(admin.ModelAdmin):
    list_display = ['commission_per_ticket']

    def has_add_permission(self, request):
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'product_id', 'type', 'amount', 'date_time_created', 'phone_number', 'status'
    ]
admin.site.register(TermsAndConditions)
