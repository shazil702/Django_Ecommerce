from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Prod_Coupon(models.Model):
    coupon_name = models.CharField(max_length=200)
    coupon_code = models.CharField(max_length=16, unique=True)
    coupon_discount = models.FloatField()
    coupon_from = models.DateTimeField()
    coupon_to = models.DateTimeField()
    coupon_min_amount = models.FloatField(default=1)
    coupon_maxuse = models.FloatField(default=1)
    active = models.BooleanField()
    user = models.ForeignKey(User, null=True, blank=True,  on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.coupon_name
class Product(models.Model):
    LIVE=1
    DELETE=0
    STATUS_CHOICES = (
        (LIVE, 'Live'),
        (DELETE, 'Delete'),
    )    
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=250)
    product_price = models.FloatField()
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images')
    product_category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    product_status = models.IntegerField(choices=STATUS_CHOICES,default=LIVE)
    
    def __str__(self):
        return self.product_name

class Cart_Product(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.product_name