from django.contrib import admin
from . models import Product,Cart_Product
from Checkout.models import Adress

# Register your models here.

admin.site.register(Product)

admin.site.register(Cart_Product)

admin.site.register(Adress)
