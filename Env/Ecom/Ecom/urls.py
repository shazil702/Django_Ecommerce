"""
URL configuration for Ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Mainapp import views
from Mainapp.views import Shop
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('search/', views.search, name='search'),
    path('product-single/<int:pk>/', views.product_single, name='product-single'),
    path('shop/', Shop.as_view(), name='shop'),
    path('category/<str:pk>/', views.category, name='category'),
    path('search_price/', views.search_price, name='search_price'),
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:pk>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:pk>/',views.remove_cart,name='remove_cart'),
    path('add_cart_quantity/<int:pk>/',views.add_cart_quantity,name='add_cart_quantity'),
    path('delete_cart/<int:pk>/',views.delete_cart, name='delete_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('get_address/<int:pk>/', views.get_address, name='get_address'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('contact/', views.contact, name='contact'),
    path('login/',(views.login_page), name='login'),
    path('register/',(views.register), name='register'),
    path('logout/', views.logout_page, name='logout'),
    

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
