# Generated by Django 5.0.4 on 2024-04-27 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_sale_price_alter_variation_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='stock',
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=1, help_text='Available stock of the product'),
        ),
    ]
