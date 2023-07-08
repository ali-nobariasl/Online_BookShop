from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import VendorForm
from accounts.forms import UserProfileForm

from .models import Vendor
from accounts.models import UserProfile
from accounts.views import check_role_vendor

from stok.models import Category , BookItem


def get_vendor(request):
    vendor = Vendor.objects.get(user= request.user)
    return vendor


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



def menu_builder(request):
    
    vendor = Vendor.objects.get(user= request.user)
    categories = Category.objects.filter(vendor=vendor)


    context = {'categories': categories}    
    return render(request, 'vendor/menu_builder.html' , context=context)



def bookitems_by_category(request, pk):
    
    vendor = Vendor.objects.get(user= request.user)
    try:
        category = Category.objects.get(vendor=vendor, pk = pk)
    except:
        category= None
        
    items = BookItem.objects.filter(category= category)
    context = {'items': items,
               'category': category}
    return render(request, 'vendor/bookitems_by_category.html',context= context)