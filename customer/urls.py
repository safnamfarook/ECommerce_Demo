from django import views
from django.urls import path
from . import views

app_name='customer'

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('verifyotp', views.verify_otp, name='verify_otp'),
    path('home',views.customer_home,name='cust_home'),
    path('logout',views.cust_logout,name='logout'),
    path('search', views.search_products, name='search'),
    path('product/<int:id>', views.view_product, name='view_product'),
    path('add-to-bag', views.add_to_bag, name="add_to_bag"),
    path('bag', views.view_bag, name="bag"),
    path('update-qty', views.update_quantity, name="update_qty"),
    path('order-product', views.order_product, name='order_product'),
    path('update-payment', views.update_payment, name='update_payment'),
    path('my-orders', views.view_orders, name='my_orders'),
    path('change-passwd', views.change_password, name='change_passwd'),
    path('profile', views.view_profile, name='profile'),
    path('edit-profile', views.update_profile, name='update_profile'),
    path('password-otp', views.send_otp, name='send_otp'),
    path('forgot-passwd', views.forgot_passwd, name='forgot'),
    path('check_avilable/',views.check_avilable,name="check_available")



]