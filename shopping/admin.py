from django import forms
from django.contrib import admin
from django.db.models import Prefetch

from products.models import Product
from .models import Purchase, PurchaseItem

# Clase base para ModelAdmin que establece campos como de solo lectura basándose en los permisos del usuario.
class ViewOnlyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('app_label.can_change_model_name'):
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

# Formulario para PurchaseItem
class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ('product', 'quantity')

# Formulario para Purchase
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('supplier', 'tax', 'purchase_type', 'state', 'delivery_date')

# Formset para PurchaseItem con lógica de validación personalizada
class PurchaseItemFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

# Inline para PurchaseItem que utiliza el formset personalizado
class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    formset = PurchaseItemFormSet
    extra = 1

# Configuración del panel de administración para Purchase
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    form = PurchaseForm
    readonly_fields = ('purchase_date', 'total') # Campos de solo lectura
    inlines = [PurchaseItemInline]
    list_display = ('supplier', 'total', 'state', 'purchase_date', 'delivery_date')
    list_filter = ('supplier', 'state')
    search_fields = ('supplier__name',)
    
    def get_queryset(self, request):
        # Optimización de consultas utilizando select_related
        return super().get_queryset(request).select_related('supplier')

# Configuración del panel de administración para PurchaseItem
@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    form = PurchaseItemForm
    list_display = ('purchase', 'product', 'quantity', 'subtotal')
    list_filter = ('purchase__supplier', 'product')
    
    def get_queryset(self, request):
        # Optimización de consultas utilizando prefetch_related
        return super().get_queryset(request).prefetch_related(
            Prefetch('product', queryset=Product.objects.select_related('category'))
        )
