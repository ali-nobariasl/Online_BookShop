from django.shortcuts import render

from vendor.models import Vendor


def index(request):
    
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[0:8]
    print(vendors)
    context = {
        'vendors': vendors,
    }
    return render(request,'home.html', context=context)