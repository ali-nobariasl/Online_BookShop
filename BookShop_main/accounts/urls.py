from django.urls import path , include

from .views import registerUser ,registerVendor



urlpatterns = [
    
    path('registeruser/', registerUser, name='registerUser'),
    path('registerVendor/', registerVendor, name='registerVendor'),
    
]
