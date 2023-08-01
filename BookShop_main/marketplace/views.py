from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime
# geometry
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance
#from geoapp.models import SouthTexasCity

# mine
from vendor.models import Vendor , OpeningHour
from stok.models import Category, BookItem
from .models import Cart
from .context_processors import get_cart_counter ,get_cart_amounts

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
    
    opening_hours=OpeningHour.objects.filter(vendor=vendor).order_by('day','from_hour')
    
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    is_open = None
    for i in current_opening_hours:
        start = str(datetime.strptime(i.from_hour, '%I:%M %p').time())
        end = str(datetime.strptime(i.to_hour, '%I:%M %p').time())
        if current_time < end and current_time > start:
            is_open = True
        else:
            is_open = False
   
        
        
        
        
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
        
    context = {'vendor':vendor,
               'categories':categories,
               'cart_items':cart_items,
               'opening_hours':opening_hours,
               'current_opening_hours':current_opening_hours,
               'is_open':is_open,}
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
                                         'qty':chkcat.quantity,
                                         'cart_amount':get_cart_amounts(request),})
                except:
                    chkcat = Cart.objects.create(user= request.user, bookitem=bookitem, quantity=1)
                    return JsonResponse({'status':'Success','message':'cart created and quantity increased',
                                         'cart_counter':get_cart_counter(request),
                                         'qty':chkcat.quantity,
                                         'cart_amount':get_cart_amounts(request)})
                    
            except:
                return JsonResponse({'status':'failed','message':'this item is not exist'})
        else:
            return JsonResponse({'status':'failed','message':'Invalid request.'})     
    else:
        return JsonResponse({'status':'login_required','message':'Please log in, before any actions.'})


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
                                        'qty':chkcat.quantity,
                                        'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'failed','message':'you dont have this in.'})    
            except:
                return JsonResponse({'status':'failed','message':'this item is not exist'})
        else:
            return JsonResponse({'status':'failed','message':'Invalid request.'}) 
    else:
        return JsonResponse({'status':'login_required','message':'Please log in, before any actions.'})
    
    
@login_required(login_url='login')
def cart(request):
    
    cartitems = Cart.objects.filter(user = request.user).order_by('created_at')
    context = {'cartitems': cartitems}
    return render(request,'marketplace/cart.html',context=context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                item = Cart.objects.get(user=request.user, id=cart_id)
                if item:
                    item.delete()
                    return JsonResponse({'status':'Success','message':'cart deleted successfully',
                                         'cart_counter':get_cart_counter(request),
                                         'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'failed','message':'this item is not exist'})
        else:
            return JsonResponse({'status':'failed','message':'Invalid request.'}) 
        
        

def search(request):
    if not 'address' in request.GET:
        return redirect(marketplace)
    else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']  
        keyword = request.GET['keyword']
        
        # get the vendor id that has item user need
        fetch_vendor_by_bookitems= BookItem.objects.filter(book_title__icontains=keyword,
                                                is_available=True).values_list('vendor',flat=True)

        vendors = Vendor.objects.filter(Q(id__in = fetch_vendor_by_bookitems)|Q(vendor_name__icontains=keyword,
                                        is_approved=True,user__is_active=True))
        
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s  %s)' % (longitude, latitude ))    
            vendors = Vendor.objects.filter(Q(id__in = fetch_vendor_by_bookitems)|Q(vendor_name__icontains=keyword,
            is_approved=True,user__is_active=True))
            
            for v in vendors:
                v.kms =v.distance.km
        vendor_count = vendors.count()
        context = {'vendors':vendors,
                'vebdor_count':vendor_count,
                'source_location':address,
                }
    return render(request,'marketplace/listing.html',context= context)