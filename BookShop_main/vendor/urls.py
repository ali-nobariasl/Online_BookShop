from django.urls import path , include

from . import views
from accounts import views as AccountViews



urlpatterns = [
    
    
    path('', AccountViews.vendorDashboard,name='vendor'),
    path('profile/', views.vprofile,name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>', views.bookitems_by_category, name='bookitems_by_category'),
    
    ## Category CRUD
    path('menu-builder/category/add', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    ## Book Item CRUD
    path('menu-builder/book/add', views.add_book, name='add_book'),
    path('menu-builder/book/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('menu-builder/book/delete/<int:pk>/', views.delete_book, name='delete_book'),
    
    ## Opening hours CRUD
    path('opening-hours/',views.opening_hours, name='opening_hours'),
    path('opening-hours/add/',views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/',views.remove_opening_hours, name='remove_opening_hours'),
    
    path('order_detail/<int:order_number>/', views.order_detail,name="vendor_order_detail"),
    
]