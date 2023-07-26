from django.shortcuts import render
# geometry
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance


from vendor.models import Vendor


def index(request):
    
    if 'lat' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']
        
        pnt = GEOSGeometry('POINT(%s  %s)' % (lng, lat ))    
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt,D(km=1000))).annotate(
            distance=Distance("user_profile__location",pnt)).order_by("distance")
            
        for v in vendors:
                v.kms =v.distance.km
    else:   
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[0:8]
    context = {
        'vendors': vendors,
    }
    return render(request,'home.html', context=context)