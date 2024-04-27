from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Supplier, Product, Variation

# Configuración del panel de administración para la categoría
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    """
    Administración de categorías utilizando MPTTModelAdmin para aprovechar las funcionalidades de MPTT.
    """
    list_display = ('name', 'parent') # Campos a mostrar en la lista de categorías
    search_fields = ('name',) # Campos para búsqueda
    list_filter = ('parent',) # Filtros disponibles en la lista de categorías
    list_per_page = 15 # Número de categorías por página en la lista

# Configuración básica del panel de administración para el proveedor
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Administración de proveedores con configuración básica.
    """
    list_display = ('name', 'url', 'supplier_type') # Campos a mostrar en la lista de proveedores
    search_fields = ('name', 'url', 'supplier_type') # Campos para búsqueda
    list_filter = ('supplier_type',) # Filtros disponibles en la lista de proveedores

# Configuración personalizada del panel de administración para el producto
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Administración de productos con campos relevantes incluidos.
    """
    list_display = ('name', 'category', 'supplier', 'purchase_price', 'sale_price', 'offer_price', 'created_at', 'updated_at', 'stock') # Campos a mostrar en la lista de productos
    search_fields = ('name', 'description') # Campos para búsqueda
    list_filter = ('category', 'supplier', 'created_at', 'updated_at') # Filtros disponibles en la lista de productos
    readonly_fields = ('created_at', 'updated_at') # Campos de solo lectura
    list_per_page = 15 # Número de productos por página en la lista
    ordering = ('name', 'category', 'supplier', 'purchase_price', 'sale_price', 'offer_price', 'created_at', 'updated_at', 'stock') # Campos a mostrar en la lista de productos

    # Métodos personalizados para calcular y mostrar el margen de beneficio
    def profit_margin(self, obj):
        return obj.profit_margin()
    profit_margin.short_description = 'Margen de beneficio'

    def total_profit_margin(self, obj):
        return Product.total_profit_margin()
    total_profit_margin.short_description = 'Margen de beneficio total'

# Configuración personalizada del panel de administración para la variación
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    """
    Administración de variaciones con información relevante mostrada.
    """
    list_display = ('name', 'product', 'category', 'state') # Campos a mostrar en la lista de variaciones
    search_fields = ('name', 'product__name') # Campos para búsqueda
    list_filter = ('category', 'state') # Filtros disponibles en la lista de variaciones
