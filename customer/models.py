import datetime
import imp
from django.db import models
from reseller.models import Products, Resellers
# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=30,db_column='f_name')
    last_name = models.CharField(max_length=30,db_column='l_name')
    mobile = models.CharField(max_length=12,db_column='mob')
    gender = models.CharField(max_length=6,db_column='gender')
    dob = models.DateField(db_column='dob')
    address = models.CharField(max_length=70,db_column='addr')
    country = models.CharField(max_length=30,db_column='cntry')
    user_type = models.CharField(max_length=10,db_column='u_type')
    email = models.CharField(max_length=50,db_column='email')
    passwd = models.CharField(max_length=50,db_column='passwd')
    otp = models.CharField(max_length=70,db_column='otp')
    status = models.CharField(max_length=20, default="",db_column='status')

    class Meta:
        db_table="customer"


class Orders(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE,db_column='p_id')
    reseller = models.ForeignKey(Resellers, on_delete=models.CASCADE,db_column='reseller',null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,db_column='c_id')
    order_date = models.DateField(default=datetime.date.today,db_column='ord_date')
    qty = models.IntegerField(db_column='qty')
    status = models.CharField(max_length=30,db_column='status')

    class Meta:
        db_table="orders"