from django.db import models
from django.utils.text import slugify
from django.db.models import F, Sum, Count
from mptt.models import MPTTModel, TreeForeignKey

# Modelo para categorías de productos, utilizando MPTTModel para estructura de árbol
class Category(MPTTModel):
    name = models.CharField(max_length=100, db_index=True) # Nombre de la categoría
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children') # Categoría padre

    class MPTTMeta:
        order_insertion_by = ['name'] # Orden de inserción por nombre

    class Meta:
        db_table = "Categories"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

# Modelo para proveedores
class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True) # Nombre del proveedor
    url = models.URLField(blank=True, null=True, help_text="URL of the supplier's online store") # URL de la tienda en línea
    supplier_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of supplier (e.g., wholesaler, retailer)") # Tipo de proveedor
    description = models.TextField(blank=True, null=True, help_text="Brief description of the supplier") # Descripción del proveedor
    image = models.ImageField(upload_to='suppliers/', blank=True, null=True, help_text="Image representing the supplier") # Imagen del proveedor

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Suppliers"

# Modelo para productos
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='products', help_text="Product Category", db_index=True) # Categoría del producto
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, related_name='products', help_text="Product supplier", db_index=True) # Proveedor del producto
    name = models.CharField(max_length=100, db_index=True, help_text="Product name") # Nombre del producto
    description = models.TextField(help_text="Product description") # Descripción del producto
    purchase_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, help_text="Product purchase price") # Precio de compra del producto
    sale_price = models.DecimalField(default=0.00, blank=True, max_digits=10, decimal_places=2, help_text="Product sale price") # Precio de venta del producto
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text="Product offer price") # Precio de oferta del producto
    slug = models.SlugField(max_length=255, unique=True, editable=False) # Slug único para la URL del producto
    created_at = models.DateTimeField(auto_now_add=True) # Fecha de creación del producto
    updated_at = models.DateTimeField(auto_now=True) # Fecha de última actualización del producto
    image = models.ImageField(upload_to='products/', blank=True, null=True) # Imagen del producto
    stock = models.PositiveIntegerField(default=1, help_text="Available stock of the product") # Stock disponible del producto
    
    def __str__(self):
        return self.name
    
    def profit_margin(self):
        if self.sale_price > 0:
            return ((self.sale_price - self.purchase_price) / self.sale_price) * 100
        return 0
    
    @staticmethod
    def total_profit_margin():
        total_profit = Product.objects.aggregate(total_profit=Sum(F('sale_price') - F('purchase_price')))['total_profit']
        total_products = Product.objects.count()
        if total_products > 0:
            return total_profit / total_products
        return 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)

    class Meta:
        ordering = ['name', 'category']
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = "Products"

# Modelo para variaciones de productos
class Variation(models.Model):
    VAR_CATEGORIES = [
        ('size', 'Size'),
        ('color', 'Color'),
    ]
    STATE = [
        ('available', 'Available'),
        ('not available', 'Not available'),
        ('deleted', 'Deleted'),
    ]
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE) # Producto asociado
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size') # Categoría de la variación
    name = models.CharField(max_length=120, help_text="Variation name") # Nombre de la variación
    state = models.CharField(max_length=120, choices=STATE, default='available') # Estado de la variación

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Variations"
