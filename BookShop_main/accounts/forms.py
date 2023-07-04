from django import forms

from .models import User, UserProfile




class UserForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        
    def clean(self):
        clean_data =super(UserForm,self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("passi jun is not match :)")
        
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model= UserProfile
        fields = ['profile_picture','cover_photo','address_line_1','address_line_2', 'country','state','city','pin_code','latitude','longitude']