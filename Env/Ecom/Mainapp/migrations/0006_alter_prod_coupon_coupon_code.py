# Generated by Django 5.0.1 on 2024-02-19 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0005_remove_prod_coupon_user_prod_coupon_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prod_coupon',
            name='coupon_code',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
