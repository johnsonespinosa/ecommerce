from django.db import models
from products.models import Product, Supplier


class Purchase(models.Model):
    STATE = [
        ('canceled', 'Canceled'),
        ('finished', 'Finished'),
        ('pending', 'Pending')
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    state = models.CharField(max_length=120, choices=STATE, default='finished')
    purchase_date = models.DateTimeField(auto_now_add=True, help_text="Purchase date")
    delivery_date = models.DateField(null=True, blank=True, help_text="Delivery date")

    @property
    def total(self):
        # Calculates the total of the purchase by adding the subtotals of all the items.
        return sum(item.subtotal for item in self.items.all()) + self.tax

    def __str__(self):
        # String representation of the Purchase object.
        return f"{self.state} - {self.total}"

    class Meta:
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'
        db_table = "Purchases"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_items')
    quantity = models.PositiveIntegerField(default=1, help_text='Quantity of product')

    @property
    def subtotal(self):
        # Calculates the subtotal of the purchase item.
        return self.product.purchase_price * self.quantity

    def __str__(self):
        # String representation of the PurchaseItem object.
        return f"{self.purchase.purchase_date} - {self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'purchase item'
        verbose_name_plural = 'purchase items'
        db_table = "PurchaseItems"
