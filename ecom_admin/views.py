import imp
from django.shortcuts import render
from reseller.models import Resellers
# Create your views here.

def home(request):
    
    return render(request,'admin_home.html')

def reseller_request(request):
    request_data=Resellers.objects.filter(status='inactive')

    if request.method=='POST':

        rqst=request.POST['req_id']
        reseller=Resellers.objects.get(id=rqst)

        if 'approve' in request.POST:
            reseller.status='active'
            
        if 'reject' in request.POST:
            reseller.status='reject'
        
        reseller.save()
    return render(request,'resellers_request.html',{'request_data':request_data,})


def view_resellers(request):
    resellers=Resellers.objects.filter(status='active')
    print(resellers)
    return render(request,'view_resellers.html',{'resellers':resellers,})
