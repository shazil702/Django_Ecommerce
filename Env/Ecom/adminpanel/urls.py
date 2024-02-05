from .views import *
from django.urls import path

app_name = 'adminpanel'

urlpatterns=[
    path('index',admin_index,name='admin_index'),
    path('accounts',admin_accounts,name='admin_accounts'),
    path('products',admin_products,name='admin_products'),
    path('add',admin_add,name='admin_add'),
    path('edit/<int:pk>',admin_edit,name='admin_edit'),
    path('',admin_login,name='admin_login'),
    path('logout',admin_logout,name='admin_logout'),
    path('delete_products',admin_delete_products,name='admin_delete_products'),
   
]