# Generated by Django 5.0.4 on 2024-04-26 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0003_supplier_description_supplier_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correlative_number', models.CharField(max_length=20, null=True, unique=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('purchase_type', models.CharField(blank=True, help_text='Type of purchase (e.g., regular, emergency)', max_length=100, null=True)),
                ('state', models.CharField(choices=[('canceled', 'Canceled'), ('finished', 'Finished')], default='finished', max_length=120)),
                ('purchase_date', models.DateTimeField(auto_now_add=True, help_text='Purchase date')),
                ('delivery_date', models.DateField(blank=True, help_text='Delivery date', null=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='products.supplier')),
            ],
            options={
                'verbose_name': 'purchase',
                'verbose_name_plural': 'purchases',
                'db_table': 'Purchases',
            },
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(help_text='Quantity of product')),
                ('subtotal', models.DecimalField(decimal_places=2, help_text='Subtotal', max_digits=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, help_text='Purchase price per unit', max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_items', to='products.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shopping.purchase')),
            ],
            options={
                'verbose_name': 'purchase item',
                'verbose_name_plural': 'purchase items',
                'db_table': 'PurchaseItems',
            },
        ),
    ]