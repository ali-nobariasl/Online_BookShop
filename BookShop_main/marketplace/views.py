from django.shortcuts import render


from vendor.models import Vendor


def marketplace(request):
    
    
    marketplace = Vendor.objects.filter()
    context = {'marketplace':marketplace}
    return render(request, 'marketplace/listing.html', context=context)