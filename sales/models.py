from django.db import models
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator

from products.models import Product, Inventory


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
                              help_text="Enter customer email", validators=[EmailValidator()])
    address = models.TextField(verbose_name="Address", help_text="Enter the customer's address")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="The phone number must be in the format: '+999999999'. Up to 15 digits are allowed."
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
        ('finished', 'Finished'),
        ('pending', 'Pending')
    ]
    shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='sales',
                                 help_text="Customer associated with the sale", db_index=True)
    sale_date = models.DateTimeField(auto_now_add=True, help_text="Sale date", db_index=True)
    state = models.CharField(max_length=120, choices=STATE, default='finished')

    @property
    def total(self):
        # Calculates the total of the purchase by adding the subtotals of all the items.
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Sale {self.state} - {self.total}"

    class Meta:
        verbose_name = 'sale'
        verbose_name_plural = 'sales'
        db_table = "Sales"


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sale_items',
                                help_text="Product sold", db_index=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, related_name='items',
                             help_text="Sale to which the item belongs", db_index=True)
    quantity = models.IntegerField(default=1, null=True, blank=True, help_text="Number of products sold")
    sale_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, help_text="Sale price")

    @property
    def subtotal(self):
        # Calculates the subtotal of the purchase item.
        return self.sale_price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'sale item'
        verbose_name_plural = 'sale items'
        db_table = "SaleItems"


class Return(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_process', 'In Process'),
        ('processed', 'Processed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='returns')
    reason = models.TextField()
    date_returned = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


