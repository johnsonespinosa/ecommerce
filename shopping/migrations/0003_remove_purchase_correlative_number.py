# Generated by Django 5.0.4 on 2024-04-27 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_remove_purchase_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='correlative_number',
        ),
    ]
