from django.core.cache import cache

from products.models import Inventory


def get_inventory_items():
    items = cache.get('inventory_items')
    if not items:
        items = Inventory.objects.all()
        cache.set('inventory_items', items)
    return items
