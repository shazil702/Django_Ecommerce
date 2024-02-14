
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from . models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from Checkout.models import *
import razorpay
from django.views.decorators.cache import never_cache
from django.utils import timezone

# Create your views here.
def about(request):
    return render(request, 'about.html')

def shop(request):
    get_product= Product.objects.all()
    return render(request,'shop.html',{'get_products':get_product})

def search(request):
    if request.method == 'POST':
        query = request.POST['search_product']
        get_product = Product.objects.filter(product_name__icontains=query)
        return render(request, 'search.html',{'get_products':get_product})

def blog(request):
    return render(request, 'blog.html')

@login_required(login_url='login')                                                                                                                                                                                                                                                                                                                                                                                                                              
def cart(request):
    items= Cart_Product.objects.filter(user=request.user)
    total_price= sum((item.product.product_price * item.quantity ) for item in items)
    all_total = total_price+60

    request.session['total_price']= total_price
    request.session['all_total']= all_total

    return render(request, 'cart.html', {'items': items, 'total_price':total_price, 'all_total':all_total})

@login_required(login_url='login')
def add_cart(request, pk):
    product=Product.objects.get(product_id=pk)
    user=request.user
    if Cart_Product.objects.filter(user=user,product=product).exists():
        item=Cart_Product.objects.get(user=user,product=product)
        item.quantity+=1
        item.save()
    else:
        Cart_Product.objects.create(user=user,product=product,quantity=1)
    return redirect('cart')

def remove_cart(request, pk):
    product=Product.objects.get(product_id=pk)
    user=request.user
    if Cart_Product.objects.filter(user=user,product=product).exists():
        item=Cart_Product.objects.get(user=user,product=product)
        item.quantity-=1
        item.save()
        if item.quantity==0:
            item.delete()
    return JsonResponse({'quantity': item.quantity, 'product_price':item.product.product_price})

def add_cart_quantity(request, pk):
    product=Product.objects.get(product_id=pk)
    user=request.user
    if Cart_Product.objects.filter(user=user,product=product).exists():
        item=Cart_Product.objects.get(user=user,product=product)
        item.quantity+=1
        item.save()
    return JsonResponse({'quantity': item.quantity, 'product_price':item.product.product_price})
def delete_cart(request, pk):
    product=Product.objects.get(product_id=pk)
    user=request.user
    item=Cart_Product.objects.get(user=user,product=product)
    item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    total_price = request.session.get('total_price', 0)
    all_total = request.session.get('all_total', 0)
    if request.method == 'POST':
        adress_name = request.POST['firstname']
        adress_lastname = request.POST['lastname']
        adress_state = request.POST['state']
        adress_house = request.POST['streetaddress']
        adress_area = request.POST['area']
        adress_city = request.POST['city']
        adress_phone = request.POST['phone']
        adress_pincode = request.POST['pincode']
        adress_user = request.user
        adress = Adress(adress_name=adress_name,adress_lastname=adress_lastname,adress_state=adress_state,adress_house=adress_house,adress_area=adress_area,adress_city=adress_city,adress_phone=adress_phone,adress_pincode=adress_pincode,adress_user=adress_user)
        adress.save()

        
        
        client = razorpay.Client(auth=("rzp_test_6gQ0trEdPai7zw", "8BPqLZ2nzJMX3sobgMMic4W2"))
        order_amount = int(all_total*100)
        order_currency = 'INR'
        order_receipt = f'order_receipt_{Adress.adress_id}'[:40]
        order = client.order.create({
            "receipt": order_receipt,
            "amount": order_amount,
            "currency": order_currency,
            "payment_capture": 1,
           
        })
        return render(request, 'checkout.html', { 'order_id': order['id'], 'razorpay_key': 'rzp_test_6gQ0trEdPai7zw'})
    
    active_coupon = Coupon.objects.filter(active = True, coupen_from__lte = timezone.now(), coupen_to__gte = timezone.now())
   
    return render(request, 'checkout.html', {'total_price' : total_price, 'all_total': all_total, 'active_coupon': active_coupon})

def apply_coupon(request):
    total_price = request.session.get('total_price', 0)
    all_total = request.session.get('all_total', 0)
    if request.method == 'POST':
        code = request.POST['coupon_code']
        coupon = Coupon.objects.get(coupen_code=code, active = True, coupen_from__lte = timezone.now(), coupen_to__gte = timezone.now())
        total_price = total_price - coupon.coupen_discount
        all_total = all_total - coupon.coupen_discount
        return render(request, 'checkout.html', {'total_price': total_price, 'all_total': all_total})

def contact(request):
    return render(request,'contact.html')

def index(request):
    get_product= Product.objects.all()
    return render(request, 'index.html',{'get_products':get_product})

def product_single(request,pk):
    get_product=Product.objects.filter(product_id=pk)
    return render(request, 'product-single.html',{'get_products':get_product})
    
@never_cache
def login_page(request):
    
    error_message= None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user and user.is_superuser:
            login(request,user)
            return redirect('adminpanel:admin_login')
        if user is not None:
            login(request,user)
            return redirect('index')
       
        else:
            error_message = "Invalid Details"
    return render(request, 'login.html',{'error_message':error_message})


def register(request):
     if request.method == 'POST':
        Name = request.POST['Name']
        username = request.POST['username']
        Email = request.POST['Email']
        password = request.POST['password']
        check_user =User.objects.filter(username=username)
        if check_user:
            messages.info(request,"Username already exists")
        else:
            user = User.objects.create_user(username=username,password=password,email=Email,first_name=Name)
            user.save()
            return redirect('login')
     return render(request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def category(request,pk):
    get_cat = Category.objects.get(name=pk)
    get_product=Product.objects.filter(product_category=get_cat)
    return render(request, 'category.html',{'get_products':get_product, 'get_cat':get_cat})
def search_price(request):
    if request.method == 'POST':
       min_range = int(request.POST['from'])
       max_range = int(request.POST['to'])
       products = Product.objects.filter(product_price__range=(min_range,max_range))
       if products.exists():
        return render(request,'category.html', {'get_products':products, 'min':min_range ,'max':max_range })
       else:
           error_message = 'No such product'
           return render(request,'shop.html',{'error_message':error_message})
    error_message = 'No such product'
    return render(request,'shop.html',{'error_message':error_message})

