from django.shortcuts import render , get_object_or_404
from django.contrib import messages

from .forms import VendorForm
from accounts.forms import UserProfileForm

from .models import Vendor
from accounts.models import UserProfile


def vprofile(request):
    
    
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user = request.user)
    
    profile_form = UserProfileForm(instance= profile)
    vendor_form = VendorForm(instance=vendor)
    
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,)
        vendor_form = VendorForm(request.POST)
        if vendor_form.is_valid() and profile_form.is_valid():
            vendor_form.save()
            profile_form.save()
            
        else:
            messages.error(request,'Invalid profile')
        
        
            
    
    
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        
    }
    return render(request, 'vendor/vprofile.html', context=context)