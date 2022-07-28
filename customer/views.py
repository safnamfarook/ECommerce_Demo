from random import randint
import razorpay
from tracemalloc import get_traced_memory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from reseller.models import Resellers
# from ..reseller import models
# from e_commerce.reseller.models import Resellers
from django.utils.crypto import get_random_string

from reseller.models import Resellers,Products
from .models import *

# Create your views here.

def index(request):
    return render(request,'customer/index.html')


def signup(request):

    if request.method=='POST':

        user_type=request.POST['user_type']
        
        if user_type=='customer':
            first_name=request.POST['first_name'].lower()
            last_name=request.POST['last_name'].lower()
            gender=request.POST['gender']
            dob=request.POST['dob']
            addr=request.POST['addr']
            country=request.POST['country']
            mobile=request.POST['mobile']
            email=request.POST['email']
            password=request.POST['password']
            
            customer_exist=Customer.objects.filter(email=email).exists()

            if not customer_exist:
                otp = randint(1000, 9999)
                send_mail(
                    'please verify your otp',
                    str(otp),
                    settings.EMAIL_HOST_USER,
                    [email],
                    
                )
                customer_data=Customer(first_name=first_name,last_name=last_name,gender=gender,
                user_type=user_type,email=email,dob=dob,address=addr,country=country,mobile=mobile,passwd=password,status='otpverify', otp=str(otp))
                customer_data.save()
                customer=Customer.objects.get(email=email)
                request.session['cust_id']=customer.id
                return redirect('customer:verify_otp')

        if user_type=='reseller':

            cmp_name=request.POST['cmp_name']
            cmp_reg=request.POST['cmp_reg']
            cmp_addr=request.POST['addr']
            country=request.POST['country']
            mobile=request.POST['mobile']
            email=request.POST['email']
            acc_holder=request.POST['acc_name']
            acc_no=request.POST['acc_no']
            acc_ifsc=request.POST['acc_ifsc']
            password=request.POST['password']
            log_id=randint(1000, 9999)

            reseller_exist=Resellers.objects.filter(email=email).exists()

            if not reseller_exist:
                reseller=Resellers(cmp_name=cmp_name,company_regid=cmp_reg,cmp_addr=cmp_addr,
                country=country,cmp_phno=mobile,acc_no=acc_no,acc_holder=acc_holder,acc_ifsc=acc_ifsc,user_type=user_type,
                email=email,user_id=log_id,passwd=password)

                reseller.save()
                subject='You Login ID is '+str(log_id)
                send_mail(
                    'login credentials',
                    subject,
                    settings.EMAIL_HOST_USER,
                    [email],
                    
                )
                msg='Registration Successfull'
            else:
                msg='Email Exist'   
            return render(request,'customer/signup.html',{'msg':msg})

    return render(request,'customer/signup.html')

def login(request):

    if request.method=='POST':
        
        user_name=request.POST['user_name']
        passwd=request.POST['passwd']
       
        if '@' in user_name:
            customer_exist=Customer.objects.filter(email=user_name,passwd=passwd).exists()
            print(customer_exist)
            if customer_exist:
                
                customer=Customer.objects.get(email=user_name,passwd=passwd)
                request.session['cust_id']=customer.id
                if customer.status=='otpverify':
                   
                    otp = randint(1000, 9999)
                    send_mail(
                        'please verify your otp',
                        str(otp),
                        settings.EMAIL_HOST_USER,
                        [customer.email],
                        fail_silently=False,
                    )
                    customer.otp=otp
                    customer.save()
                    return redirect('customer:verify_otp')
                return redirect('customer:cust_home')
            else:
                return render(request, 'customer/login.html', {'error': 'Invalid user details'})
                
        elif user_name.isdigit():

            seller_exist=Resellers.objects.filter(user_id=user_name,passwd=passwd).exists()
            
            if seller_exist:
                seller_data=Resellers.objects.get(user_id=user_name,passwd=passwd)
               
                if seller_data.status=='active':
                    
                    request.session['s_id']=seller_data.id
                    return redirect('reseller:reseller_home')
                
                else: 
                    return render(request, 'customer/login.html', {'error': 'Account Not Approved Yet'})
            
            else:
                    return render(request, 'customer/login.html', {'error': 'UserName Or Password Incorrect'})
    return render(request,'customer/login.html')

def verify_otp(request):
    
    if request.method=='POST':

        otp = request.POST['inp_otp']
        c_id=request.session['cust_id']
        data=Customer.objects.get(id=c_id)
       
        if otp==data.otp:
            Customer.objects.filter(id=c_id).update(status='active')
            return redirect('customer:cust_home')
        else:
            return render(request, "customer/verify_otp.html", {"msg": "Invalid otp"})
    return render(request,'customer/verify_otp.html')

def customer_home(request):
    return render(request,'customer/home.html')

def search_products(request):
    # search data based on keyword
    if request.method == "POST":
        search_word = request.POST['searchdata']
        # search_list=search_word.split(' ')
        print(search_word)
        srch_products=Products.objects.filter(Q(vendor__icontains=search_word)|Q(title__icontains=search_word)| Q(category__icontains=search_word)|Q(subcategory__icontains=search_word),status='active' )

      
        print(srch_products)
        # Rendering search product page
        return render(request, "customer/search_products.html",{"search_products":srch_products})
    else:
        return redirect('customer:index')


def view_product(request,id):
    product = Products.objects.get(id=id)
    return render(request, "customer/view_product.html",{ 'product': product, })


def add_to_bag(request):

    prod_id=Products.objects.get(id=request.POST['id'])
    reseller_id=Resellers.objects.get(id=prod_id.reseller.id)
    quantity=request.POST['quantity']
    cust_id=Customer.objects.get(id=request.session['cust_id'])
    data_exist=Orders.objects.filter(customer_id=request.session['cust_id'],product_id=prod_id)
    if not data_exist:
        order_data=Orders(product_id=prod_id,qty=quantity,customer_id=cust_id,status='added_to_bag',reseller=reseller_id    )
        order_data.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})


def cust_logout(request):
    if 'cust_id' in request.session:
        del request.session['cust_id']
        request.session.flush()
    return redirect('customer:cust_home')


def view_bag(request):
    total=0
    if request.method == 'POST':
        pass
        # cust_id = request.session['cust_id']
        # bagdata = Orders.objects.filter(customerid=cust_id, status='added_to_bag')
        # bag_ids = bagdata.values_list('product_id_id')
        # productdata = Products.objects.filter(id__in=bag_ids)
        # bgdata=[{'email': usr.email, 'joindate': usr.date_joined} for bg in bgdata]
    else:
        cust_id = request.session['cust_id']
        bag_data = Orders.objects.filter(customer_id=cust_id, status='added_to_bag')
        # bag_ids = bag_data.values_list('product_id_id')
        # products = Products.objects.filter(id__in=bag_ids)
        # price = 0
        # for prod in products:
        #     for bg in bag_data:
        #         if bg.product_id_id == prod.id:
        #             price = price + (bg.qty * prod.price)
        # print(price)

        for prod in bag_data:
            price=prod.product_id.price*prod.qty
            total+=price

        return render(request,"customer/view_bag.html",{'bag_data': bag_data,  'total': total})


def update_quantity(request):

    total=0
    qty=request.GET['qty']
    order_id=request.GET['ord_id']
    order_detail=Orders.objects.get(id=order_id)
    order_detail.qty=qty
    
    order_detail.save()
    product_total=order_detail.product_id.price* int(qty)
    bag_data = Orders.objects.filter(customer_id=request.session['cust_id'],status='added_to_bag')
    for prod in bag_data:
            price=prod.product_id.price*prod.qty
            total+=price
   
    print('***********',product_total)
    return JsonResponse({"total": total,"product_total":product_total})


def order_product(request):

    order_amount = request.POST['total']
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    notes = {'Shipping address': 'Bommanahalli, Bangalore'}
    type(order_amount)
    client = razorpay.Client(auth=('rzp_test_jznmHCFBf6ZMUd','hMGwzenl3b1QwDmJxDtyAUNy'))
    payment = client.order.create({"amount": order_amount, "currency": order_currency, "receipt": order_receipt, 'notes': notes})
    return JsonResponse( payment)


def update_payment(request):

    print('reached here')
    Orders.objects.filter(customer_id=request.session['cust_id'], status='added_to_bag').update(status='paid')
    return JsonResponse({'resp': "success"})


def view_orders(request):

    cust_id = request.session['cust_id']
    bag_data = Orders.objects.filter(customer_id=cust_id, status='paid')
    return render(request,"customer/view_orders.html",{'bag_data': bag_data, })


def change_password(request):
    
    cust_data = Customer.objects.get(id=request.session['cust_id'])

    if request.method=='POST':
        password=request.POST['password']
        otp=request.POST['otp']

        if cust_data.otp==otp:
            cust_data.passwd=password
            cust_data.save()
            return JsonResponse({'res':'Password Updated','status':'success'})
        
        else:
            return JsonResponse({'res':'Invalid Otp','status':'error'})
    
    return render(request, "customer/change_password.html",{'msg':'Otp has been sent to your email',})


def view_profile(request):
    id = request.session['cust_id']
    customer_data = Customer.objects.get(id=id)
    return render(request, 'customer/profile.html', {'profile': customer_data,})

def update_profile(request):
    fname = request.POST['firstname']
    lname = request.POST['lastname']
    address = request.POST['address']
    country = request.POST['country']
    mobile = request.POST['mobile']
    id = request.session['cust_id']
    # User.objects.filter(id=id).update(first_name=fname, last_name=lname)
    Customer.objects.filter(id=id).update(first_name=fname, mobile=mobile, address=address, country=country,)
    custdata = Customer.objects.get(id=id)
    customerdata = {'firstname': custdata.first_name,'lastname': custdata.last_name, 'gender': custdata.gender, 'dateofbirth': custdata.dob, 'mobile': custdata.mobile, 'address': custdata.address, 'country': custdata.country,'email': custdata.email}
    # userdata = User.objects.get(id=id)
    # usrdata = {'lastname': userdata.last_name, 'email': userdata.email }
    return JsonResponse({"custdata": customerdata, })

def send_otp(request):
    cust_data = Customer.objects.get(id=request.session['cust_id'])

    # if request.method=='POST':

    #     password=request.POST['password']
    #     otp=request.POST['otp']

    #     if cust_data.otp==otp:
    #         cust_data.passwd=password
    #         cust_data.save()
    #         return JsonResponse({'res':'Password Updated','status':'success'})
    #     else:
    #         return JsonResponse({'res':'Invalid Otp','status':'error'})

    customer_email=cust_data.email
    otp = randint(1000, 9999)
    send_mail(
            'verify otp',
            str(otp),
            settings.EMAIL_HOST_USER,
            [customer_email],
            
        )
    cust_data.otp=otp
    cust_data.save()
    return redirect('customer:change_passwd')

def forgot_passwd(request):
    return render(request,'customer/forgot_passwd.html')

def check_avilable(request):
    email=request.GET["email"]
   
    date_avilble=Customer.objects.filter(email=email).exists()
    
   
    return JsonResponse({'isAvailable': date_avilble})