
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

from marketplace.views import cart
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
    
    path('marketplace/', include('marketplace.urls')),
    
    # cart
    path('cart/', cart, name='cart'),             
        
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
