# Generated by Django 5.0.4 on 2024-04-26 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_shipping_alter_customer_phone_number_sale_shipping'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='shipping',
            table='Shipments',
        ),
    ]
