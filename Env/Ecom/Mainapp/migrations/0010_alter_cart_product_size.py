# Generated by Django 5.0.1 on 2024-02-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0009_cart_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_product',
            name='size',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
