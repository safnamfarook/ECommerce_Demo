from django import views
from django.urls import path
from . import views

app_name='reseller'

urlpatterns = [

    path('reseller-home',views.reseller_home,name='reseller_home'),
    path('add-product',views.add_product,name='add_product'),
    path('all-products',views.view_products,name='view_products'),
    path('product/<int:id>/',views.edit_product,name='edit_product'),
    path('update-product',views.update_product,name='update_product'),
    path('product-del',views.delete_product,name='del_product'),
    path('orders',views.view_orders,name='orders'),
    path('logout',views.logout,name='logout')


]