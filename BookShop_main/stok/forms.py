from django import forms

from .models import Category, BookItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','description')
        
        
class BookItemForm(forms.ModelForm):
    class Meta:
        model =BookItem
        fields =('category','book_title','writer','description',
                 'price','image','is_available')