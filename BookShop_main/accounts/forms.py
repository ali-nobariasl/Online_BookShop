from django import forms

from .models import User, UserProfile
from accounts.validators import allow_only_images_validator



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
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
    address =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typing...','required':'required'}))
    #latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model= UserProfile
        fields = ['profile_picture','cover_photo','address', 'country','state','city','pin_code','latitude','longitude']
        
    
    def __init__(self,*args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
            
            
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']