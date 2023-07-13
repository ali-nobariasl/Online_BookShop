from django.shortcuts import render,get_object_or_404,HttpResponse
from django.db.models import Prefetch

from vendor.models import Vendor
from stok.models import Category, BookItem



def marketplace  (request):
    
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {'vendors':vendors,
               'vendor_count':vendor_count,
               }
    return render(request, 'marketplace/listing.html', context=context)




def vendor_detail(request,vendor_slug):
    
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug )
    
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'bookitems',      ## this is related name
            queryset= BookItem.objects.filter(is_available=True)
        )
    )
    context = {'vendor':vendor,
               'categories':categories}
    return render(request, 'marketplace/vendor_detail.html', context=context)



def add_to_cart(request,book_id):
    
    return HttpResponse("testing")