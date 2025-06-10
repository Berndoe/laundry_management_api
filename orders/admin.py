from django.contrib import admin
from .models import Orders, OrderItem



# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'status', 'company']
    search_fields = list_display
    ordering = list_display


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity', 'company']
    search_fields = list_display
    ordering = list_display


admin.site.register(Orders, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
