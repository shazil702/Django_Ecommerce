# Generated by Django 5.0.1 on 2024-01-23 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=250)),
                ('product_price', models.FloatField()),
                ('product_description', models.TextField()),
                ('product_image', models.ImageField(upload_to='product_images')),
                ('product_status', models.IntegerField(choices=[(1, 'Live'), (0, 'Delete')], default=1)),
            ],
        ),
    ]
