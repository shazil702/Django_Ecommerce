from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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