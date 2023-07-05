from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import VendorForm
from accounts.forms import UserProfileForm

from .models import Vendor
from accounts.models import UserProfile
from accounts.views import check_role_vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user = request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance= profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance= vendor)
        
        if vendor_form.is_valid() and profile_form.is_valid():
            vendor_form.save()
            profile_form.save()
            messages.success(request,'Your store has been updated successfully')   
            return redirect('vprofile')   
        else:
            messages.error(request,'Invalid profile')
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance= profile)
        vendor_form = VendorForm(instance=vendor)  
            
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        
    }
    return render(request, 'vendor/vprofile.html', context=context)