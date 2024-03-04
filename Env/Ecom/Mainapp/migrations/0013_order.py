# Generated by Django 5.0.1 on 2024-02-26 11:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkout', '0002_remove_adress_adress_email_adress_adress_user'),
        ('Mainapp', '0012_alter_cart_product_size'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=30)),
                ('amount', models.FloatField(default=1)),
                ('payment_status', models.BooleanField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Checkout.adress')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mainapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]