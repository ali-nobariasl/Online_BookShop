from django.shortcuts import render, redirect
from  django.contrib import messages, auth
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify

from .forms import UserForm
from .models import User , UserProfile
from .utils import detectUrl , send_verification_email
from orders.models import Order
from vendor.forms import VendorForm
from vendor.models import Vendor


# restrict the vendor from accessing the customer page 
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# restrict the customer from accessing the vendor page 
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
    

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"you are already logged in.")
        return redirect('myAccount')
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
            
            #send verification email
            mail_subject ='Please Activate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, mail_template)
            
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
        return redirect('myAccount')
    elif request.method == 'POST':
        v_form = VendorForm(request.POST, request.FILES)
        form = UserForm(request.POST)
        
        if (form.is_valid()) and (v_form.is_valid()):
            
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
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+ '-' + str(user.id)
            vendor.save()
                        
            #send verification email
            mail_subject ='Please Activate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, mail_template)
            
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



@login_required(login_url='login')
def myAccount(request):
    
    user = request.user
    redirectUrl = detectUrl(user)
    return redirect( redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {'recent_orders':recent_orders,
               'orders_count': orders.count(),
               }
    print(orders)
    return render(request, 'accounts/custDashboard.html',context=context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
    recent_orders = orders[:5]
    print("orders are ---->",orders)
    
    context= {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders':recent_orders,
    }
    return render(request, 'accounts/vendorDashboard.html', context=context)



def activate(request,uidb64,token):
    # activate the user 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(ValueError, TypeError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your account activated successfully')
        return redirect('myAccount')
    else:
        messages.error(request,'the verification link is not correct')
        return redirect('myAccount')


def forgotPassword(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if  User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            #send reset password link via email
            mail_subject ='Reset Your Password'
            mail_template = 'accounts/emails/password_reset_email.html'
            send_verification_email(request, user, mail_subject, mail_template)
            
            messages.success(request,'password reset link has been sent to your mail.')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotPassword')
        
    return render(request,'accounts/emails/forgotPassword.html')



def resetPasswordValidate(request, uidb64,token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(ValueError, TypeError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
       request.session['uid'] = uid
       messages.success(request,'Please reset your password')
       return redirect('resetPassword')
    else:
       messages.error(request,'This link has been expired. Please try again')
       return redirect('myAccount')



def resetPassword(request):
    
    if request.method == 'POST':
        confirm_password = request.POST.get('confirm_password')
        password = request.POST.get('password')
        pk = request.session.get('uid')
        if confirm_password == password:
            user = User._default_manager.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request,'Passwords not match. Please try again')
            return redirect('resetPassword')
        
    return render(request, 'accounts/emails/resetPassword.html')