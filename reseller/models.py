from datetime import datetime
from django.db import models

# Create your models here.

class Resellers(models.Model):

    cmp_name = models.CharField(max_length=30,db_column='c_name')
    company_regid = models.CharField(max_length=12,db_column='reg_id')
    cmp_addr = models.CharField(max_length=70,db_column='addr')
    country = models.CharField(max_length=30,db_column='cntry')
    cmp_phno = models.CharField(max_length=12,db_column='phno')
    acc_holder = models.CharField(max_length=30,db_column='acc_hld')
    acc_no = models.CharField(max_length=30,db_column='acc_no')
    acc_ifsc = models.CharField(max_length=30,db_column='ifsc')
    user_type = models.CharField(max_length=20,db_column='type')
    email=models.CharField(max_length=30,db_column='email')
    passwd=models.CharField(max_length=30,db_column='passwd')
    user_id = models.IntegerField(db_column='log_id')
    request_date = models.DateField(default=datetime.now)
    status = models.CharField(max_length=20, default= 'inactive')

    class Meta:
        db_table='resellers'


class Products(models.Model):
    title = models.CharField(max_length=30,db_column='title')
    reg_product_id = models.CharField(max_length=12,db_column='p_id')
    desc = models.TextField(db_column='desc')
    img = models.ImageField(upload_to = 'product_images/', blank = True, null = True,db_column='img')
    price = models.IntegerField(db_column='price')
    quantity = models.IntegerField(db_column='qty')
    weight = models.IntegerField(db_column='wt')
    weight_unit = models.CharField(max_length=12,db_column='unit')
    category = models.CharField(max_length=12,db_column='cat')
    subcategory = models.CharField(max_length=12,db_column='sub_cat')
    vendor = models.CharField(max_length=100,db_column='vendor')
    status = models.CharField(max_length=100,db_column='status')
    reseller = models.ForeignKey(Resellers, on_delete=models.CASCADE,db_column='reseller')

    class Meta:
        db_table='products'