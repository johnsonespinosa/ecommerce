from django.db import models
from django_extensions.db.fields import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey


# Model for product categories, using MPTTModel for tree structure
class Category(MPTTModel):
    # Category name
    name = models.CharField(max_length=100, db_index=True)
    # Parent Category
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        # Insertion order by name
        order_insertion_by = ['name']

    class Meta:
        db_table = "Categories"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


# Model for suppliers
class Supplier(models.Model):
    # Provider's name
    name = models.CharField(max_length=255, unique=True, db_index=True)
    # Online store URL
    url = models.URLField(blank=True, null=True,
                          help_text="URL of the supplier's online store")
    # Provider type
    supplier_type = models.CharField(max_length=100, blank=True, null=True,
                                     help_text="Type of supplier (e.g., wholesaler, retailer)")
    # Provider Description
    description = models.TextField(blank=True, null=True,
                                   help_text="Brief description of the supplier")
    # Provider Image
    image = models.ImageField(upload_to='suppliers/', blank=True, null=True,
                              help_text="Image representing the supplier")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Suppliers"


# Model for products
class Product(models.Model):
    # Product category
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='products',
                                 help_text="Product Category", db_index=True)
    # Product supplier
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, related_name='products',
                                 help_text="Product supplier", db_index=True)
    # Product name
    name = models.CharField(max_length=100, db_index=True, help_text="Product name")
    # Product description
    description = models.TextField(help_text="Product description")
    # Product purchase price
    purchase_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2,
                                         help_text="Product purchase price")
    # Sales price of the product
    sale_price = models.DecimalField(default=0.00, blank=True, max_digits=10, decimal_places=2,
                                     help_text="Product sale price")
    # Unique slug for product URL
    slug = AutoSlugField(populate_from='name', unique=True)
    # Product creation date
    created_at = models.DateTimeField(auto_now_add=True)
    # Product image
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def stock(self):
        return sum(inventory.current_stock for inventory in self.inventories.all())

    @property
    def profit_margin(self):
        if self.sale_price > 0:
            return ((self.purchase_price - self.sale_price) / self.purchase_price) * 100
        return 0

    class Meta:
        ordering = ['name', 'category']
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = "Products"


# Model for product variations
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
    # Associated product
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    # Variation Category
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    # Variation name
    name = models.CharField(max_length=120, help_text="Variation name")
    # Variation status
    state = models.CharField(max_length=120, choices=STATE, default='available')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Variations"


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    current_stock = models.PositiveIntegerField(default=0, help_text="Available stock of the product")
    min_stock = models.PositiveIntegerField(default=0, help_text="Minimum stock of the product")
    max_stock = models.PositiveIntegerField(default=0, help_text="Maximum stock of the product")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.current_stock}"

    class Meta:
        db_table = "Inventories"
        verbose_name = "inventory"
        verbose_name_plural = "inventories"


class ProductIssue(models.Model):
    PRODUCT_ISSUE_TYPES = [
        ('default', 'Default'),
        ('imperfect', 'Imperfect'),
        ('damaged', 'Damaged'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='issue')
    issue_type = models.CharField(max_length=20, choices=PRODUCT_ISSUE_TYPES, default='default')
    notes = models.TextField(blank=True, null=True, help_text="Additional details about the issue")

    def __str__(self):
        return f"{self.product.name} - {self.issue_type}"

    class Meta:
        db_table = "ProductIssues"
        verbose_name = "product issue"
        verbose_name_plural = "product issues"
