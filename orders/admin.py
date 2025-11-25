from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from django.urls import path
from django.utils.timezone import now, localdate
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'city', 'status', 'status_badge', 'paid_badge', 'paid', 'created', 'updated', 'total_cost']
    list_filter = ['paid', 'created', 'updated', 'city']
    search_fields = ['id', 'user__username', 'email', 'first_name', 'last_name', 'city']
    date_hierarchy = 'created'
    ordering = ['-created']
    list_select_related = ['user']
    readonly_fields = ['created', 'updated']
    list_editable = ['paid', 'status']
    inlines = [OrderItemInline]

    actions = ['delete_selected', 'mark_as_paid', 'mark_as_unpaid', 'set_pending', 'set_processing', 'set_shipped', 'set_delivered', 'set_canceled', 'export_orders_csv', 'delete_old_orders']
    actions_on_top = True
    actions_on_bottom = True

    def total_cost(self, obj):
        return obj.get_total_cost()
    total_cost.short_description = 'Total'

    def paid_badge(self, obj):
        if obj.paid:
            return format_html('<span class="badge-paid">PAID</span>')
        return format_html('<span class="badge-unpaid">UNPAID</span>')
    paid_badge.short_description = 'Status'

    def status_badge(self, obj):
        cls = {
            'pending': 'badge-pending',
            'processing': 'badge-processing',
            'shipped': 'badge-shipped',
            'delivered': 'badge-delivered',
            'canceled': 'badge-canceled',
        }.get(obj.status, 'badge-pending')
        return format_html('<span class="{}">{}</span>', cls, obj.get_status_display())
    status_badge.short_description = 'Stage'

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(paid=True)
        self.message_user(request, f"Marked {updated} order(s) as paid.")
    mark_as_paid.short_description = 'Mark selected orders as paid'

    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(paid=False)
        self.message_user(request, f"Marked {updated} order(s) as unpaid.")
    mark_as_unpaid.short_description = 'Mark selected orders as unpaid'

    def export_orders_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'User', 'Email', 'First name', 'Last name', 'City', 'Paid', 'Created', 'Updated', 'Total'])
        for o in queryset.select_related('user'):
            writer.writerow([
                o.id,
                o.user.username if o.user_id else '',
                o.email,
                o.first_name,
                o.last_name,
                o.city,
                'Yes' if o.paid else 'No',
                o.created.isoformat(),
                o.updated.isoformat(),
                o.get_total_cost(),
            ])
        return response
    export_orders_csv.short_description = 'Export selected to CSV'

    def delete_old_orders(self, request, queryset):
        from datetime import timedelta
        threshold_days = 90
        cutoff = now() - timedelta(days=threshold_days)
        old_qs = Order.objects.filter(created__lt=cutoff)
        count = old_qs.count()
        old_qs.delete()
        self.message_user(request, f"Deleted {count} order(s) older than {threshold_days} days.")
    delete_old_orders.short_description = 'Delete orders older than 90 days'

    # Bulk status actions
    def _set_status(self, request, queryset, value, label):
        updated = queryset.update(status=value)
        self.message_user(request, f"Set status '{label}' on {updated} order(s).")

    def set_pending(self, request, queryset):
        self._set_status(request, queryset, 'pending', 'Pending')
    set_pending.short_description = "Set status: Pending"

    def set_processing(self, request, queryset):
        self._set_status(request, queryset, 'processing', 'Processing')
    set_processing.short_description = "Set status: Processing"

    def set_shipped(self, request, queryset):
        self._set_status(request, queryset, 'shipped', 'Shipped')
    set_shipped.short_description = "Set status: Shipped"

    def set_delivered(self, request, queryset):
        self._set_status(request, queryset, 'delivered', 'Delivered')
    set_delivered.short_description = "Set status: Delivered"

    def set_canceled(self, request, queryset):
        self._set_status(request, queryset, 'canceled', 'Canceled')
    set_canceled.short_description = "Set status: Canceled"

    class Media:
        css = {
            'all': ('admin/admin_custom.css',)
        }
        js = (
            'admin/orders_autorefresh.js',
        )

    # Custom admin dashboard under Orders
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='orders_order_dashboard'),
        ]
        return custom + urls

    def dashboard_view(self, request):
        today = localdate()
        qs = Order.objects.all()
        stats = {
            'total_orders': qs.count(),
            'total_paid_orders': qs.filter(paid=True).count(),
            'total_unpaid_orders': qs.filter(paid=False).count(),
            'today_orders': qs.filter(created__date=today).count(),
            'today_revenue': qs.filter(paid=True, created__date=today)
                .aggregate(total=Sum(ExpressionWrapper(F('items__price') * F('items__quantity'), output_field=DecimalField(max_digits=12, decimal_places=2))))['total'] or 0,
        }

        recent = qs.select_related('user').order_by('-created')[:10]
        context = dict(
            self.admin_site.each_context(request),
            title='Orders Dashboard',
            stats=stats,
            recent_orders=recent,
        )
        from django.shortcuts import render
        return render(request, 'admin/orders/dashboard.html', context)