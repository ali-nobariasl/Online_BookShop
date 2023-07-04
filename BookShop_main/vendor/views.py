from django.shortcuts import render
from django.contrib import messages

from .forms import VendorForm
from accounts.forms import UserProfileForm



def vprofile(request):
    
    profile_form = UserProfileForm()
    vendor_form = VendorForm()
    
    
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
    }
    return render(request, 'vendor/vprofile.html', context=context)