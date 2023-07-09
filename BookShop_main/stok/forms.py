from django import forms

from .models import Category, BookItem
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','description')
        
        
class BookItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}))
    
    class Meta:
        model =BookItem
        fields =('category','book_title','writer','description',
                 'price','image','is_available')