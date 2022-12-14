# Generated by Django 4.0.2 on 2022-07-27 05:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reseller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_column='f_name', max_length=30)),
                ('last_name', models.CharField(db_column='l_name', max_length=30)),
                ('mobile', models.CharField(db_column='mob', max_length=12)),
                ('gender', models.CharField(db_column='gender', max_length=6)),
                ('dob', models.DateField(db_column='dob')),
                ('address', models.CharField(db_column='addr', max_length=70)),
                ('country', models.CharField(db_column='cntry', max_length=30)),
                ('user_type', models.CharField(db_column='u_type', max_length=10)),
                ('email', models.CharField(db_column='email', max_length=50)),
                ('passwd', models.CharField(db_column='passwd', max_length=50)),
                ('otp', models.CharField(db_column='otp', max_length=70)),
                ('status', models.CharField(db_column='status', default='', max_length=20)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(db_column='ord_date', default=datetime.date.today)),
                ('qty', models.IntegerField(db_column='qty')),
                ('status', models.CharField(db_column='status', max_length=30)),
                ('customer_id', models.ForeignKey(db_column='c_id', on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('product_id', models.ForeignKey(db_column='p_id', on_delete=django.db.models.deletion.CASCADE, to='reseller.products')),
                ('reseller', models.ForeignKey(db_column='reseller', null=True, on_delete=django.db.models.deletion.CASCADE, to='reseller.resellers')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
