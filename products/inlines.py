from django.contrib import admin

from products.models import Variation


# Inline for product variations
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1
    max_num = 5