from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction

from products.models import Inventory
from .models import Return, Sale


@receiver(post_save, sender=Sale)
def update_inventory_on_sale(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            for item in instance.saleitem_set.all():
                product_id = item.product.id
                try:
                    inventory_data = cache.get(f'inventory:{product_id}')
                    if inventory_data:
                        current_stock = inventory_data
                    else:
                        inventory = Inventory.objects.get(product=item.product)
                        current_stock = inventory.current_stock
                        cache.set(f'inventory:{product_id}', current_stock, timeout=300)

                    new_stock = current_stock - item.quantity
                    cache.set(f'inventory:{product_id}', new_stock, timeout=300)
                    inventory.current_stock = new_stock
                    inventory.save()
                    cache.delete(f'inventory:{product_id}')  # # Invalidate cache after update
                except Inventory.DoesNotExist:
                    print(f"Product with ID {product_id} not found in inventory.")


@receiver(pre_save, sender=Return)
def update_inventory_on_return(sender, instance, **kwargs):
    if instance.status == 'returned':
        inventory = Inventory.objects.get(product=instance.product)
        inventory.current_stock += instance.product.quantity
        inventory.save()


@receiver(pre_save, sender=Sale)
def check_stock_availability(sender, instance, **kwargs):
    """
    Check if the total quantity of products in the sale does not exceed the available stock.
    """
    inventory_items = Inventory.objects.only('product', 'current_stock').prefetch_related('product').filter(
        product__in=instance.saleitem_set.values_list('product', flat=True))

    for item in instance.saleitem_set.all():
        inventory_item = next((i for i in inventory_items if i.product == item.product), None)
        if inventory_item and item.quantity > inventory_item.current_stock:
            raise ValidationError(f"The stock of the product {item.product.name} is insufficient to complete the sale.")
