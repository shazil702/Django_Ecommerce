from django.contrib import admin
from . models import *
from Checkout.models import Adress

# Register your models here.

admin.site.register(Product)

admin.site.register(Cart_Product)

admin.site.register(Category)

admin.site.register(Coupon)

admin.site.register(Adress)
