# Generated by Django 5.0.1 on 2024-03-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0015_remove_order_address_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(editable=False, max_length=25, unique=True),
        ),
    ]