# Generated by Django 5.0.1 on 2024-03-01 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkout', '0002_remove_adress_adress_email_adress_adress_user'),
        ('Mainapp', '0014_remove_order_address_remove_order_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Checkout.adress'),
        ),
    ]
