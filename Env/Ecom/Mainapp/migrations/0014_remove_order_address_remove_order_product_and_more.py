# Generated by Django 5.0.1 on 2024-02-28 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkout', '0002_remove_adress_adress_email_adress_adress_user'),
        ('Mainapp', '0013_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ManyToManyField(to='Checkout.adress'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='Mainapp.product'),
        ),
    ]
