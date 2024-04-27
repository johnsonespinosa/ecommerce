from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product, Supplier

class Purchase(models.Model):
    STATE = [
        ('canceled', 'Canceled'),
        ('finished', 'Finished')
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of purchase (e.g., regular, emergency)")
    state = models.CharField(max_length=120, choices=STATE, default='finished')
    purchase_date = models.DateTimeField(auto_now_add=True, help_text="Purchase date")
    delivery_date = models.DateField(null=True, blank=True, help_text="Delivery date")
    
    @property
    def total(self):
        """Calcula el total de la compra sumando los subtotales de todos los items."""
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        """Representación en cadena del objeto Purchase."""
        return f"{self.state} - {self.total}"
    


    class Meta:
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'
        db_table = "Purchases"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_items')
    quantity = models.PositiveIntegerField(help_text='Quantity of product')
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item de compra."""
        return self.product.purchase_price * self.quantity

    def __str__(self):
        """Representación en cadena del objeto PurchaseItem."""
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'purchase item'
        verbose_name_plural = 'purchase items'
        db_table = "PurchaseItems"
        
@receiver(post_save, sender=Purchase)
def update_stock_after_purchase_save(sender, instance, created, **kwargs):
    if created:
        # Actualización del stock y creación de nuevos productos si no existen
        products_to_update = []
        for item in instance.items.all():
            product, created = Product.objects.get_or_create(
                name=item.product.name,
                defaults={'purchase_price': item.product.purchase_price}
            )
            if not created:
                product.stock += item.quantity
                products_to_update.append(product)
        
        Product.objects.bulk_update(products_to_update, ['stock'])
