from django.shortcuts import render, redirect
from  django.contrib import messages
from .forms import UserForm
from .models import User


def registerUser(request):
    
    if request.method == 'POST':
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
            user = User.objects.create(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account was created successfully')
            return redirect('registerUser')
        else:
            print("form is not valid")
            print(form.errors)
    else:      
        form = UserForm()
        
        
    
    context ={
        'form': form,
        'form_errors': form.errors
    }
    return render(request, 'accounts/register.html',context)
