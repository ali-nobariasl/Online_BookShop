from django.shortcuts import render






def cprofile(request):
    
    context = {}
    return render(request, 'customers/cprofile.html', context=context)