
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from . models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Checkout.models import Adress
import razorpay
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.mail import send_mail
import random
from django.conf import settings

# Create your views here.
def about(request):
    return render(request, 'about.html')


class Shop(ListView):
    model=Product
    template_name='shop.html'
    context_object_name = 'get_products'
    paginate_by=6



def search(request):
    if request.method == 'POST':
        query = request.POST['search_product']
        get_product = Product.objects.filter(product_name__icontains=query)
        return render(request, 'search.html',{'get_products':get_product})



def blog(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'blog.html', {'orders':orders})



@login_required(login_url='login')                                                                                                                                                                                                                                                                                                                                                                                                                              
def cart(request):
    items= Cart_Product.objects.filter(user=request.user)
    total_price= sum((item.product.product_price * item.quantity ) for item in items)
    all_total = total_price+60
    request.session['total_price']= total_price
    request.session['all_total']= all_total
    return render(request, 'cart.html', {'items': items, 'total_price':total_price, 'all_total':all_total})


def get_total_price(request):
    items= Cart_Product.objects.filter(user=request.user)
    total_price= sum((item.product.product_price * item.quantity ) for item in items)
    all_total = total_price+60
    request.session['total_price']= total_price
    request.session['all_total']= all_total
    return JsonResponse({'total_price':total_price, 'all_total':all_total})



@login_required(login_url='login')
def add_cart(request, pk):
    product=Product.objects.get(product_id=pk)
    user=request.user
    if request.method == 'POST':
        size = request.POST['size']
        quantity = int(request.POST.get('quantity'))
        if Cart_Product.objects.filter(user=user,product=product).exists():
            item=Cart_Product.objects.get(user=user,product=product)
            item.quantity += quantity
            item.size = size
            item.save()
        else:
            Cart_Product.objects.create(user=user,product=product,quantity=quantity,size=size)
        return redirect('cart')   
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
        if item.quantity < 1:
            item.quantity = 1
            item.save()
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
    response ={'success': False}
    if Cart_Product.objects.filter(user=user,product=product).exists():
        item=Cart_Product.objects.get(user=user,product=product)
        item.delete()
        response['success']=True
    return JsonResponse(response)


def address(request):
    user = request.user
    adressess = Adress.objects.filter(adress_user=user)
    if request.method == 'POST':
        adress_name = request.POST['firstname']
        
        adress_lastname = request.POST['lastname']
        adress_state = request.POST['state']
        adress_house = request.POST['streetaddress']
        adress_area = request.POST['area']
        adress_city = request.POST['city']
        adress_phone = request.POST['phone']
        adress_pincode = request.POST['pincode']
        adress_user = user
        adress, created = Adress.objects.get_or_create(adress_name=adress_name,adress_lastname=adress_lastname,adress_state=adress_state,adress_house=adress_house,adress_area=adress_area,adress_city=adress_city,adress_phone=adress_phone,adress_pincode=adress_pincode,adress_user=adress_user)
        if created:
            adress.save()
        request.session['address_id']=adress.adress_id
        return redirect('checkout')
    return render(request, 'address.html', {'adressess':adressess})
    

@login_required(login_url='login')
def checkout(request):
    total_price = request.session.get('total_price', 0)
    all_total = request.session.get('all_total', 0)
    user = request.user
    items= Cart_Product.objects.filter(user=user)
    adressess = Adress.objects.filter(adress_user=user)
    if request.method == 'POST':    
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
    user_used = Prod_Coupon.objects.filter(user=user).exists()
    if user_used:
        return render(request, 'checkout.html', {'total_price' : total_price, 'all_total': all_total,  'adressess': adressess})
    active_coupons = Prod_Coupon.objects.filter(active=True, coupon_from__lte=timezone.now(), coupon_to__gte=timezone.now(), coupon_min_amount__lte=total_price)
    return render(request, 'checkout.html', {'active_coupon': active_coupons, 'total_price': total_price, 'all_total': all_total, 'adressess': adressess, 'items':items})


def get_address(request,pk):
    try:
        adress = Adress.objects.get(adress_id=pk)
        return JsonResponse({'adress_name': adress.adress_name, 'adress_lastname': adress.adress_lastname, 'adress_state': adress.adress_state, 'adress_house': adress.adress_house, 'adress_area': adress.adress_area, 'adress_city': adress.adress_city, 'adress_phone': adress.adress_phone, 'adress_pincode': adress.adress_pincode})
    except Adress.DoesNotExist:
        return JsonResponse({'error': 'Adress does not exist'}, status=404)



def apply_coupon(request):
    total_price = request.session.get('total_price',0)
    all_total = request.session.get('all_total',0)
    items= Cart_Product.objects.filter(user=request.user)
    if request.method == 'POST':
        code = request.POST['coupon_code']
        coupon = Prod_Coupon.objects.get(coupon_code=code, active=True, coupon_from__lte = timezone.now(), coupon_to__gte = timezone.now())
        all_total = all_total - coupon.coupon_discount
        coupon_disc = coupon.coupon_discount
        msg = "Coupon applied successfully"
        return render(request, 'checkout.html', {'messages':msg, 'total_price':total_price,'all_total':all_total, 'coupon_disc':coupon_disc, 'items':items })
    

@method_decorator(csrf_exempt, name='dispatch')
class Success(View):
    model=Product
    template_name='success.html'
    
    def order(self, request):
        all_total = request.session.get('all_total',0)
        adress = request.session.get('address_id',0)
        user = request.user
        try:
            
            address_instance = Adress.objects.get(adress_id=adress)
            order = Order.objects.create(
                user=user,
                amount = all_total,
                payment_status=True,
                address=address_instance
                
            )
            
            for cart_item in Cart_Product.objects.filter(user=user):
                prod_instance = cart_item.get_product_instance()
                order.product.add(prod_instance)
            order.save()
            return redirect('success')
        except (Product.DoesNotExist, Adress.DoesNotExist)as e:
            return JsonResponse({'error': str(e)}, status=400)
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        self.order(request)
        return redirect('success')
    

def index(request):
    get_product= Product.objects.all().order_by('-product_id')[:4]
    return render(request, 'index.html',{'get_products':get_product})



def product_single(request,pk):
    get_product=Product.objects.filter(product_id=pk)
    return render(request, 'product-single.html',{'get_products':get_product})
    
@never_cache
def login_page(request):
    error_message= None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        # if user and user.is_superuser:
        #     login(request,user)
        #     return redirect('admin:index')
        if user is not None:
            login(request,user)
            return redirect('index')
       
        else:
            error_message = "Invalid Details"
    return render(request, 'login.html',{'error_message':error_message})
def create_otp():
    digits = '0123456789'
    return ''.join(random.choices(digits, k=6))

def send_otp(request):
    otp = create_otp()
    request.session['otp']=otp
    email = request.POST['Email']
    subject = 'Your otp'
    message = 'your otp is ' + otp
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])

def register(request):
     if request.method == 'POST':
        Name = request.POST['Name']
        username = request.POST['username']
        Email = request.POST['Email']
        password = request.POST['password']
        check_user =User.objects.filter(email=Email)
        if check_user:
            messages.info(request,"Username already exists")
        else:
            # otp = create_otp()
            # print(otp)
            send_otp(request)
            
            request.session['Name']=Name
            request.session['username']=username
            request.session['Email']=Email
            request.session['password']=password
            return redirect('otp_check')
     return render(request,'register.html')

def otp_check(request):
    if request.method == 'POST':
        user_otp = request.POST['otp']
        otp = request.session.get('otp','')
        print(user_otp)
        print(otp)
        if user_otp == otp:
            password =request.session.get('password','')
            Name = request.session.get('Name','')
            username = request.session.get('username','')
            email = request.session.get('Email','')

            user=User.objects.create_user(username=username,password=password,email=email,first_name=Name)
            user.save()
            
            return redirect('login')
        
        else:
            error_message="Inalid OTP Please Enter correct OTP"
            return render(request, 'otp.html', {'error_message':error_message})
    return render(request, 'otp.html')

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
 
