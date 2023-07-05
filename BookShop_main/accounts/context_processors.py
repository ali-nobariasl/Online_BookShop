from django.conf import settings 


from vendor.models import Vendor


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user= request.user)
    except:
        vendor = None
        
    dict ={'vendor': vendor,}
    return dict



def get_google_api(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}