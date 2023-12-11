from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm
from django.contrib import messages
from .models import *
from .models import User, Product, Brand, category
import random
from django.contrib.auth import logout,login
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime
from datetime import datetime, timedelta
from django.http import Http404
from django.http import JsonResponse
from django.urls import reverse


# Create your views here.

#------------------------------user index------------------------------------------------------------------------------
def user_index(request):
    products = Product.objects.filter(is_available=True,is_deleted=False)
    context = {
        'products': products,   
    }
    return render(request, 'userhome/index.html',context)

#---------------------------otp generate function------------------------------------------------------------------------------------- 
def generate_otp():
    otp = str(random.randint(100000, 999999))
    timestamp = str(timezone.now())  #convert datetime to string
    return otp, timestamp

#--------------------------user signup-------------------------------------------------------------------------------------------
def signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username is already existing . please choose a different username')
            return render(request, 'userhome/usersignup.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is alrady existing so Please choose another')
            return render(request, 'userhome/usersignup.html')
        elif cpassword != password:
            messages.error(request, 'mismatch password')
            return render(request, 'userhome/usersignup.html')
        #generate OTP
        otp, timestamp = generate_otp()
        
        request.session['signup_otp'] = otp  #save OTP to the session
        request.session['otp_timestamp'] = timestamp  #save the timestamp to the session

        send_mail(
            'OTP verification',
            f'your OTP for signup is : {otp}',
            'timetrixcronico@gmail.com',
            [email],
            fail_silently=True
        )
        request.session['signup_details']={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password': make_password(password),
        }
        return redirect(enter_otp)
    return render(request,'userhome/usersignup.html')

#------------------------------enter otp that we recive in the mail--------------------------------------------------------------
def enter_otp(request):
    if request.method == 'POST':
        entered_otp=request.POST.get('otp')
        stored_otp=request.session.get('signup_otp')
        timestamp_str = request.session.get('otp_timestamp')

         # Check if OTP is expired
        expiration_time = datetime.fromisoformat(timestamp_str) + timedelta(minutes=5)
        current_time = timezone.now()


        if current_time > expiration_time:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return render(request, 'userhome/otp.html')

        if entered_otp == stored_otp:
            new_user=User(
                username=request.session['signup_details']['username'],
                email=request.session['signup_details']['email'],
                first_name=request.session['signup_details']['first_name'],
                last_name=request.session['signup_details']['last_name'],
                phone=request.session['signup_details']['phone'],
                password=request.session['signup_details']['password']
            )
            new_user.save()
            login(request, new_user)

            request.session.pop('signup_otp',None)
            request.session.pop('otp_timestamp', None)
            request.session.pop('signup_details',None)
            return redirect('user_index')
        else:
            messages.error(request,'Invalid OTP. Please try again.')

    expiration_time = datetime.fromisoformat(request.session.get('otp_timestamp')) + timedelta(minutes=5)
    remaining_time = max(timedelta(0), expiration_time - timezone.now())
    remaining_minutes, remaining_seconds = divmod(remaining_time.seconds, 60)
    return render(request, 'userhome/otp.html',{'remaining_minutes': remaining_minutes, 'remaining_seconds': remaining_seconds})

#-------------------------------if the otp expire resend the otp-----------------------------------------------------------------------
def resend_otp(request):
    #check if there any existing signup session
    if 'signup_details' in request.session:
        #generate a new OTP and timestamp
        otp, timestamp = generate_otp()

        #update the session with the new OTP and timestamp
        request.session['signup_otp'] = otp
        request.session['otp_timestamp'] = timestamp

        #resend the OTP in email
        send_mail(
            'Resent OTP verification',
            f'Your new OTP for signup is: {otp}',
            'timetrixcronico@gmail.com',
            [request.session['signup_details']['email']],
            fail_silently=True
        )
        messages.info(request, 'New OTP sent. Please check your email.')
        return redirect('enter_otp')
    else:
        messages.error(request, 'No signup session found.')
        return redirect('signup')

#-------------------------------------user signin to the system----------------------------------------------------------------------------------
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        print(user)
        if user is not None and user.check_password(password):
            if user.is_active:
                login(request,user)
                return redirect('user_index')
            else:
                messages.error(request, 'Your account is not active')
        else:
            messages.error(request, 'Invalid username and password')   
    return render(request, 'userhome/userlogin.html')

#-------------------------------user signout-------------------------------------------------------------------------
def user_logout(request):
    logout(request)
    return redirect('user_login')
    # return render(request,'userhome/index.html')

#------------------------------display the all prouct in shop-------------------------------------------------------
def shop(request, category_slug=None):
    all_categories = category.objects.all()
    selected_category = None
    products = None
    product_count = None

    if category_slug:
        selected_category = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category=selected_category, is_available=True,is_deleted=False)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True,is_deleted=False)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'all_categories': all_categories,
        'selected_category': selected_category,
    }
    return render(request, 'userhome/shop.html', context)

#-------------------------click the product it view the product details--------------------------------------------------------------
def product_details(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    color_variants = ProductAttribute.objects.filter(product=single_product).select_related('color')

    context = {
        'single_product': single_product,
        'color_variants': color_variants,
       
    }
    return render(request, 'userhome/product_details.html', context)

#----------------------add-to-cart--------------------------------------

def add_to_cart(request):
    cart_p = {}
    product_id = str(request.GET['id'])
    cart_p[product_id] = {
        'image': request.GET.get('image', ''),
        'name': request.GET.get('name', ''),
        'qty': int(request.GET['qty']),
        'price': float(request.GET['price']) if request.GET['price'] else 0.0,
    }
    print(f"Product Name: {cart_p}")
    if 'cartdata' in request.session:
        if product_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[product_id]['qty'] = int(cart_p[product_id]['qty'])
            cart_data[product_id]['price'] = float(cart_p[product_id]['price'])
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p

    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


#------------------------------cart-list page----------------------------------------------------------------

def cart_list(request):
    total_amt = calculate_total_amount(request.session['cartdata'])
    return render(request, 'userhome/cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    

def calculate_total_amount(cart_data):
    total_amt = 0
    for p_id, item in cart_data.items():
        qty = int(item['qty'])
        price_str = str(item['price']).strip() if item['price'] else ''
        price = float(price_str) if price_str else 0.0
        total_amt += qty * price

    return total_amt

#------------------------delete cart-----------------------------------

def delete_cart_item(request):
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amt = calculate_total_amount(request.session['cartdata'])
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})


            
    
    