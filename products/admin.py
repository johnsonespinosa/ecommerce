from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Supplier, Product, Variation

# Para la categoría, utilizamos MPTTModelAdmin para aprovechar las funcionalidades de MPTT en el panel de administración
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

# Para el proveedor, simplemente registramos el modelo con la configuración básica
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'supplier_type')
    search_fields = ('name', 'url', 'supplier_type')
    list_filter = ('supplier_type',)

# Para el producto, personalizamos el panel de administración para incluir campos relevantes
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'purchase_price', 'sale_price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'supplier', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

# Para la variación, personalizamos el panel de administración para mostrar información relevante
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'category', 'state', 'stock')
    search_fields = ('name', 'product__name')
    list_filter = ('category', 'state')
