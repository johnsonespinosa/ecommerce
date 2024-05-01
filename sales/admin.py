from django.contrib import admin

from .forms import SaleForm
from .inlines import SaleItemInline
from .models import Sale, SaleItem, Customer, Shipping


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    form = SaleForm
    list_display = ('state', 'customer', 'total', 'sale_date')
    search_fields = ('customer__name', 'state')
    list_filter = ('state', 'customer')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'sale_price', 'subtotal')
    search_fields = ('product__name', 'sale__sale_date')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'gender')
    search_fields = ('name', 'email')


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'estimated_delivery_date')
    search_fields = ('name',)
