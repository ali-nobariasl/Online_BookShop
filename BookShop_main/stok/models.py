from django.db import models

from vendor.models import Vendor



class Category(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description= models.TextField(blank=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category_name
    
    
class BookItem(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    book_title = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique=True)
    description= models.TextField(blank=True, max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bookimages')
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.book_title