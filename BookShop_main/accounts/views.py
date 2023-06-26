from django.shortcuts import render, redirect
from  django.contrib import messages, auth

from .forms import UserForm
from .models import User , UserProfile
from .utils import detectUrl

from vendor.forms import VendorForm
from vendor.models import Vendor


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"you are already logged in.")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            #### create a new user by using form
            # user = form.save(commit=False)
            # password = form.cleaned_data['password']
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            
            #### create a new user by using model
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account was created successfully')
            return redirect('index')
        else:
            print("form is not valid")
            print(form.errors)
    else:      
        form = UserForm()
        
    context ={
        'form': form,
        'form_errors': form.errors,
    }
    return render(request, 'accounts/register.html',context)


def registerVendor(request):
    
    if request.user.is_authenticated:
        messages.warning(request,"you are already logged in.")
        return redirect('dashboard')
    elif request.method == 'POST':
        v_form = VendorForm(request.POST, request.FILES)
        form = UserForm(request.POST)
        
        if form.is_valid() and v_form.is_valid:
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
            user.role = User.VENDOR
            user.save()
            
            vendor = v_form.save(commit=False)
            user_profile= UserProfile.objects.get(user=user)
            
            vendor.user = user
            vendor.user_profile =  user_profile
            vendor.save()
            
            messages.success(request,"your account has been added successfully")
            return redirect('index')
        else: 
            print(form.errors)
            print("invalid form")
    else:
        v_form = VendorForm()
        form = UserForm()
        
    context = {'v_form': v_form,
               'form':form,}
    return render(request, 'accounts/registerVendor.html',context)


def logout(request):
    
    auth.logout(request)
    messages.info(request,"you are logged out")
    return redirect('login')


def login(request):
    
    if request.user.is_authenticated:
        messages.warning(request,"you are already logged in.")
        return redirect('myAccount')
    
    elif request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'you are logged in successfully')
            return redirect('myAccount')   
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login')
    
    context= {}
    return render(request, 'accounts/login.html',context=context)




def myAccount(request):
    
    user = request.user
    redirectUrl = detectUrl(user)
    return redirect( redirectUrl)



def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')



