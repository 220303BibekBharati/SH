from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'stripe_charge_id', 'amount', 'timestamp']
    list_select_related = ['order']
    search_fields = ['order__id', 'stripe_charge_id']
    list_filter = ['timestamp']
