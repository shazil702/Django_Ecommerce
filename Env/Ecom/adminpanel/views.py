from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from Mainapp.models import *

# Create your views here.
def admin_accounts(request):
    return render(request, 'adminpanel/accounts.html')

def admin_products(request):
    get_products=Product.objects.all()
    return render(request, 'adminpanel/products.html',{'get_products':get_products})

def admin_add(request):
    if request.method == 'POST':
        product_name = request.POST['name']
        product_price = request.POST['price']
        product_description = request.POST['description']
        product_image = request.FILES['product_image']
        new_product = Product(product_name=product_name,product_price=product_price,product_description=product_description,product_image=product_image)
        new_product.save()
        return redirect('adminpanel:admin_products')
    return render(request, 'adminpanel/add-product.html')

def admin_edit(request,pk):
    get_product=Product.objects.get(product_id=pk)
    if request.method == 'POST':
        if  'name' in request.POST:
            product_name = request.POST['name']
            get_product.product_name=product_name
        if  'price' in request.POST:
            product_price = request.POST['price']
            get_product.product_price=product_price
        if  'description' in request.POST:
            product_description = request.POST['description']
            get_product.product_description=product_description
        if 'product_image' in request.FILES:
            product_image = request.FILES['product_image']
            get_product.product_image=product_image
        
        get_product.save()
        return redirect('adminpanel:admin_products')
    context ={
        'get_product':get_product
    }
    return render(request, 'adminpanel/edit-product.html',context)

def admin_index(request):
    return render(request, 'adminpanel/index.html')

def admin_login(request):
    error_message= None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user and user.is_superuser:
            login(request,user)
            return redirect('adminpanel:admin_index')
        
       
        else:
            error_message = "Invalid Details"
    return render(request, 'adminpanel/login.html')
def admin_logout(request):
    logout(request)
    return redirect('/')

def admin_delete_products(request):
    if request.method == 'POST':
        product_ids= request.POST.getlist('selected_products')
        Product.objects.filter(product_id__in=product_ids).delete()
    return render(request, 'adminpanel/products.html')
