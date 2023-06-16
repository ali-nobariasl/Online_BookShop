from django.urls import path , include

from .views import registerUser



urlpatterns = [
    
    path('registeruser/', registerUser, name='registerUser'),
]
