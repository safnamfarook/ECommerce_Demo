from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def auth_customer(func):
    def wrap(request, *args, **kwargs):
        if 'cust_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            return redirect('customer:login')
            
    return wrap


def auth_seller(func):
    def wrap(request, *args, **kwargs):
        if 's_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            return redirect('customer:login')
            
    return wrap
