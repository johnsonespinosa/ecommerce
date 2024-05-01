from django.contrib import admin

from sales.models import SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1