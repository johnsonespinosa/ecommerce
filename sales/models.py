from django.db import models
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator

from products.models import Product


class Shipping(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Shipments"


class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=255, verbose_name="Customer Name", help_text="Enter the customer's full name")
    email = models.EmailField(null=True, blank=True, unique=True, db_index=True, verbose_name="Email",
                              help_text="Enter customer email")
    address = models.TextField(verbose_name="Address", help_text="Enter the customer's address")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener el formato: '+999999999'. Se permiten hasta 15 dígitos."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return self.name

    def to_dict(self):
        return model_to_dict(self)

    class Meta:
        db_table = "Customers"


class Sale(models.Model):
    STATE = [
        ('canceled', 'Canceled'),
        ('finished', 'Finished')
    ]
    shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    correlative_number = models.CharField(max_length=20, null=True, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='sales',
                                 help_text="Customer associated with the sale", db_index=True)
    sale_date = models.DateTimeField(auto_now_add=True, help_text="Sale date", db_index=True)
    state = models.CharField(max_length=120, choices=STATE, default='finished')
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.correlative_number:
            self.correlative_number = f"SALE-{self.id}"
        self.total = sum(item.subtotal for item in self.items.all())
        if self.shipping:
            self.total += self.shipping.cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.correlative_number} - {self.customer.name}"

    class Meta:
        verbose_name = 'sale'
        verbose_name_plural = 'sales'
        db_table = "Sales"


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sale_items',
                                help_text="Product sold", db_index=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, related_name='items',
                             help_text="Sale to which the item belongs", db_index=True)
    quantity = models.IntegerField(default=0, null=True, blank=True, help_text="Number of products sold")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product on sale")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, help_text='Subtotal')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'sale item'
        verbose_name_plural = 'sale items'
        db_table = "SaleItems"
