
from vendor.models import Vendor


def get_vendor(request):
    
    try:
        vendor = Vendor.objects.get(user= request.user)
    except:
        vendor = None
        
    dict ={
        'vendor': vendor,
    }
    
    return dict