from django.contrib import admin
from .models import Payment


# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'amount',
                    'payment_type', 'payment_status',
                    'payment_date', 'company']
    search_fields = list_display
    ordering = list_display


admin.site.register(Payment)
