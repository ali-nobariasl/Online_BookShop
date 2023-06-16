from django.shortcuts import render



def registerUser(request):
    
    context ={}
    return render(request, 'accounts/register.html',context=context)
