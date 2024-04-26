from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = "Categories"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    url = models.URLField(blank=True, null=True, help_text="URL of the supplier's online store")
    supplier_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of supplier (e.g., wholesaler, retailer)")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the supplier")
    image = models.ImageField(upload_to='suppliers/', blank=True, null=True, help_text="Image representing the supplier")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Suppliers"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='products',
                                 help_text="Product Category")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='products',
                                 help_text="Product supplier")
    name = models.CharField(max_length=100, db_index=True, help_text="Product name")
    description = models.TextField(help_text="Product description")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Product purchase price")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Product sale price")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text="Product offer price")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name', 'category']
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = "Products"


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
    product = models.ForeignKey(Product, related_name="product_attrs", on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    name = models.CharField(max_length=120, help_text="Variation name")
    state = models.CharField(max_length=120, choices=STATE, default='available')
    stock = models.PositiveIntegerField(default=1, help_text="Available stock of the product")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Variations"
