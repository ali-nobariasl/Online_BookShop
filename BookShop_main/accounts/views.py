from django.shortcuts import render

from .forms import UserForm



def registerUser(request):
    
    form = UserForm()
    context ={
        'form': form,
    }
    return render(request, 'accounts/register.html',context)
