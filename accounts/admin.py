from django.contrib import admin
from .models import Company, Employee, Customer


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'company_email', 'phone']
    search_fields = list_display
    ordering = list_display


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'contact', 'role', 'company']
    search_fields = list_display
    ordering = list_display


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'company']
    search_fields = list_display
    ordering = list_display


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
