from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.db import transaction
from products.models import Inventory
from .models import Purchase


@receiver(post_save, sender=Purchase)
def update_inventory_on_purchase(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            for item in instance.purchaseitem_set.all():
                product_id = item.product.id
                try:
                    inventory_data = cache.get(f'inventory:{product_id}')
                    if inventory_data:
                        current_stock = inventory_data
                    else:
                        inventory = Inventory.objects.get(product=item.product)
                        current_stock = inventory.current_stock
                        cache.set(f'inventory:{product_id}', current_stock, timeout=300)

                    new_stock = current_stock + item.quantity
                    cache.set(f'inventory:{product_id}', new_stock, timeout=300)
                    inventory.current_stock = new_stock
                    inventory.save()
                    cache.delete(f'inventory:{product_id}')  # Invalidate cache after update
                except Inventory.DoesNotExist:
                    print(f"Product with ID {product_id} not found in inventory.")
