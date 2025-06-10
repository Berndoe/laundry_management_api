from django.contrib import admin
from .models import Item, Service


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'company']
    search_fields = ['name']
    ordering = list_display


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'price', 'company']
    search_fields = list_display
    ordering = list_display


admin.site.register(Service, ServiceAdmin)
admin.site.register(Item, ItemAdmin)
