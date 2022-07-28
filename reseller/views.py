from itertools import product
from os import stat
import re
from django import http
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from customer.models import Orders

from e_commerce.auth_gaurd import auth_seller
from .models import *

# Create your views here.

@auth_seller
def reseller_home(request):
   
    return render(request,'reseller/home.html')

@auth_seller
def add_product(request):
    if request.method=='POST':

        title = request.POST['title'].lower()
        reg_product_id = request.POST['regproductid']
        description = request.POST['description'].lower()
        img = request.FILES['image']
        price = request.POST['price']
        quantity = request.POST['quantity']
        weight = request.POST['weight']
        weight_unit = request.POST['weightunit']
        category = request.POST['category']
        subcategory = request.POST['subcategory']
        vendor = request.POST['vendor'].lower()
        status = request.POST['status'].lower()
        reseller_id = Resellers.objects.get(id=request.session['s_id'])
        product_exist=Products.objects.filter(reg_product_id=reg_product_id)
        if not product_exist:
            product = Products(title=title, reg_product_id=reg_product_id, desc=description, img=img, price=price, quantity=quantity, weight=weight, weight_unit=weight_unit, category=category, subcategory=subcategory, vendor=vendor, status=status, reseller=reseller_id)
            product.save()
            return JsonResponse({'res':True})
        else:
            return JsonResponse({'res':False})
            
        # product_id = product.pk
        
    return render(request,'reseller/add_product.html')

@auth_seller
def view_products(request):

    products=Products.objects.filter(reseller=request.session['s_id'])
    return render(request,'reseller/all_products.html',{'products':products,})

@auth_seller
def edit_product(request,id):
    
    product=Products.objects.get(id=id)
    return render(request,'reseller/edit_product.html',{'product':product,})

@auth_seller
def update_product(request):
    if request.method == "POST":
        
        product_id = request.POST['id'].strip()
        title = request.POST['title'].strip()
        description = request.POST['description'].strip()
        price = request.POST['price'].strip()
        quantity = request.POST['quantity'].strip()
        status = request.POST['status'].strip()
        print(title,'*************************',len(title))
        Products.objects.filter(id=product_id).update(title=title,desc=description,
        price=price,quantity=quantity,status=status)
        return JsonResponse({'msg':'Update Succesfull'})
        
@auth_seller
def delete_product(request):
    
    get_id= int(request.GET['id'])
    product = Products.objects.get(id=get_id)
    product.delete()
    return JsonResponse({'msg':'Product Deleted'})


def logout(request):
    del request.session['s_id']
    request.session.flush()
    return redirect('customer:login')

def view_orders(request):
    
    order_details=Orders.objects.filter(reseller=request.session['s_id'])
    return render(request,'reseller/orders.html',{'orders':order_details})