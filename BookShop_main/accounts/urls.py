from django.urls import path , include

from . import views



urlpatterns = [
    
    path('', views.myAccount),
    
    path('registeruser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    
    path('myAccount/', views.myAccount, name='myAccount'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPasswordValidate/<uidb64>/<token>/', views.resetPasswordValidate, name='resetPasswordValidate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
    
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),
    
    
]
