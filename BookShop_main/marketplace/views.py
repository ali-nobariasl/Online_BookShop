from django.shortcuts import render,get_object_or_404
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse

from vendor.models import Vendor
from stok.models import Category, BookItem
from .models import Cart
from .context_processors import get_cart_counter

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
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
        
    context = {'vendor':vendor,
               'categories':categories,
               'cart_items':cart_items,}
    return render(request, 'marketplace/vendor_detail.html', context=context)



def add_to_cart(request,book_id):
    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                bookitem = BookItem.objects.get(id=book_id)
                # check if book has already been added to the cart before
                try:
                    chkcat = Cart.objects.get(user= request.user, bookitem=bookitem)
                    chkcat.quantity += 1
                    chkcat.save()
                    return JsonResponse({'status':'Success','message':'quantity increased',
                                         'cart_counter':get_cart_counter(request),
                                         'qty':chkcat.quantity })
                except:
                    chkcat = Cart.objects.create(user= request.user, bookitem=bookitem, quantity=1)
                    return JsonResponse({'status':'Success','message':'cart created and quantity increased',
                                         'cart_counter':get_cart_counter(request),
                                         'qty':chkcat.quantity })
                    
            except:
                return JsonResponse({'status':'failed','message':'this item is not exist'})
        else:
            return JsonResponse({'status':'failed','message':'Invalid request.'})     
    else:
        return JsonResponse({'status':'failed','message':'Please log in, bfore any actions.'})


def decrease_cart(request,book_id):
    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                bookitem= BookItem.objects.get(id=book_id)
                try:
                    chkcat = Cart.objects.get(user=request.user,bookitem=bookitem)
                    if chkcat.quantity >1:
                        chkcat.quantity -= 1
                        chkcat.save()
                    else:
                        chkcat.delete()
                        chkcat.quantity = 0
                    return JsonResponse({'status':'Success','message':'quantity decrease',
                                        'cart_counter':get_cart_counter(request),
                                        'qty':chkcat.quantity })
                except:
                    return JsonResponse({'status':'failed','message':'you dont have this in.'})    
            except:
                return JsonResponse({'status':'failed','message':'this item is not exist'})
        else:
            return JsonResponse({'status':'failed','message':'Invalid request.'}) 
    else:
        return JsonResponse({'status':'failed','message':'Please log in, bfore any actions.'})