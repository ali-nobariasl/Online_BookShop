from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from .forms import VendorForm
from accounts.forms import UserProfileForm

from .models import Vendor
from accounts.models import UserProfile
from accounts.views import check_role_vendor

from stok.models import Category , BookItem
from stok.forms import CategoryForm

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



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)


    context = {'categories': categories}    
    return render(request, 'vendor/menu_builder.html' , context=context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def bookitems_by_category(request, pk):
    
    vendor = get_vendor(request)
    try:
        category = Category.objects.get(vendor=vendor, pk = pk)
    except:
        category= None
        
    items = BookItem.objects.filter(category= category)
    context = {'items': items,
               'category': category}
    return render(request, 'vendor/bookitems_by_category.html',context= context)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, 'Category made successfully')
            return redirect('menu_builder')
        else:
            messages.error(request, 'Your data is not valid')
            
    else:
        form = CategoryForm()
                    
    context ={'form':form}
    return render(request, 'vendor/add_category.html', context=context)


def edit_category(request,pk=None):
    
    categoryinstance = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=categoryinstance)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, 'Category update successfully')
            return redirect('menu_builder')
        else:
            messages.error(request, 'Your data is not valid')
            
    else:
        form = CategoryForm(instance=categoryinstance)
                    
    context ={'form':form,
              'category':categoryinstance}
    return render(request, 'vendor/edit_category.html',context=context)