from django.db import models
from products.models import Product, Supplier

class Purchase(models.Model):
    STATE = [
        ('canceled', 'Canceled'),
        ('finished', 'Finished')
    ]
    correlative_number = models.CharField(max_length=20, null=True, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of purchase (e.g., regular, emergency)")
    state = models.CharField(max_length=120, choices=STATE, default='finished')
    purchase_date = models.DateTimeField(auto_now_add=True, help_text="Purchase date")
    delivery_date = models.DateField(null=True, blank=True, help_text="Delivery date")

    def __str__(self):
        return f"Purchase {self.id} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        if not self.correlative_number:
            self.correlative_number = f"PUR-{self.id}"
            self.total = sum(item.subtotal for item in self.items.all())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'
        db_table = "Purchases"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_items')
    quantity = models.PositiveIntegerField(help_text='Quantity of product')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, help_text='Subtotal')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Purchase price per unit')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.purchase_price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'purchase item'
        verbose_name_plural = 'purchase items'
        db_table = "PurchaseItems"
