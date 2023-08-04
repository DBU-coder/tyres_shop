from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'country', 'paid', 'created', 'order_details']
    list_filter = ['paid', 'created', 'country']
    search_fields = ['id', 'first_name', 'last_name', 'email']

    @admin.display(description='Order details')
    def order_details(self, obj):
        url = reverse('orders:admin_order_details', args=[obj.id])
        return mark_safe(f'<a href="{url}">View</a>')

