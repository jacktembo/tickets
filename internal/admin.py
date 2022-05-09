from django.contrib import admin
from .models import TermsAndConditions, All1zedBusCommission


@admin.register(All1zedBusCommission)
class All1ZedEventCommissionAdmin(admin.ModelAdmin):
    list_display = ['commission_per_ticket']

    def has_add_permission(self, request):
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

admin.site.register(TermsAndConditions)
