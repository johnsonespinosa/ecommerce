from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .forms import ProductForm
from .inlines import VariationInline
from .models import Category, Supplier, Product, Variation, Inventory, ProductIssue
from .resources import ProductResource


# Admin panel settings for categories
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_per_page = 10


# Admin panel settings for suppliers
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'supplier_type', 'description')
    search_fields = ('name', 'url', 'supplier_type')


# Admin panel settings for products
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    resource_class = ProductResource
    list_select_related = ('category', 'supplier')
    list_prefetch_related = ('variations',)
    inlines = [VariationInline]
    search_fields = ('name', 'description', 'category__name', 'supplier__name')
    list_filter = (
        ('supplier', admin.RelatedOnlyFieldListFilter),
        ('created_at', admin.DateFieldListFilter),
    )
    readonly_fields = ('created_at',)
    list_per_page = 10
    ordering = ('name', 'category', 'supplier', 'purchase_price', 'sale_price', 'created_at')
    list_display = ('name', 'category', 'supplier', 'formatted_price', 'created_at', 'stock', 'is_available')

    def is_available(self, obj):
        return obj.stock > 0

    is_available.boolean = True
    is_available.short_description = 'Available'

    def formatted_price(self, obj):
        return f"{obj.purchase_price} - {obj.sale_price} - {obj.profit_margin}"

    formatted_price.short_description = 'Price'


# Admin panel settings for variations
# @admin.register(Variation)
# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'product', 'category', 'state')
#     search_fields = ('name', 'product__name')
#     list_filter = ('category', 'state')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'current_stock', 'min_stock', 'max_stock', 'updated_at')
    search_fields = ('product__name',)


@admin.register(ProductIssue)
class ProductIssueAdmin(admin.ModelAdmin):
    list_display = ('product', 'issue_type', 'notes')
    search_fields = ('product__name', 'issue_type')
