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
from stok.forms import CategoryForm , BookItemForm

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
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')


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



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
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


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    
    categoryinstance =  get_object_or_404(Category, pk=pk)
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



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('menu_builder')
    

 
    
@login_required(login_url='login')
@user_passes_test(check_role_vendor)   
def add_book(request):
    
    if request.method == 'POST':
        form = BookItemForm(request.POST,request.FILES)
        if form.is_valid():
            book_name = form.cleaned_data['book_title']
            book = form.save(commit=False)
            book.vendor = get_vendor(request)
            book.slug = slugify(book_name)
            book.save()
            messages.success(request, 'Book added successfully')
            return redirect('bookitems_by_category', book.category.id)
        else:
            messages.error(request, 'invalide book information')
    else:
        form = BookItemForm()
    context = {'form':form,}
    return render(request, 'vendor/add_book.html', context=context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_book(request,pk=None):
    
    bookinstance = get_object_or_404(BookItem, pk=pk)
    if request.method == 'POST':
        form = BookItemForm(request.POST,request.FILES,instance=bookinstance)
        if form.is_valid():
            book_title = form.cleaned_data['book_title']
            book = form.save(commit=False)
            book.vendor = get_vendor(request)
            book.slug = slugify(book_title)
            book.save()
            messages.success(request,'Book created successfully')
            return redirect('bookitems_by_category', book.category.id)
        else:
            messages.error(request, 'invalide book information')
    else:
        form = BookItemForm(instance=bookinstance)
        
    context ={'form':form,
              'book':bookinstance}
    return render(request, 'vendor/edit_book.html',context=context)




def delete_book(request, pk=None):
    
    book = get_object_or_404(BookItem, pk=pk)
    book.delete()
    messages.success(request,'Book deleted successfully')
    
    return redirect('bookitems_by_category', book.category.id)