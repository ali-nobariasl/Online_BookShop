from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager


class USerManager(BaseUserManager): # No fields  # just methods 
    
    def create_user(self,username, first_name, last_name, email,password=None):
        
        if not email:
            raise ValueError('email must be specified! ')
        
        if not username:
            raise ValueError('username must be specified! ')
        
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    
    def craetesuperuser(self,username, first_name, last_name, email,password=None):
        
        user = self.craete_user(
            username=username,
            first_name= first_name,
            last_name= last_name,
            email=self.normalize_email(email),
            password=password)
        
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.is_stuff = True
        user.save(using=self._db)
        
        return user



class User(AbstractBaseUser):  
    
    BOOKSHOP = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (BOOKSHOP,'BOOKSHOP'),
        (CUSTOMER,'CUSTOMER'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    
    # Django required fields
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    is_admin = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff  = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username','first_name','last_name']
    
    objects = USerManager()  # this tells which class should be used for making user
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_modele_perms(self, app_label):
        return True
    
    
    
    ###### and in the setting we should change
    ###   AUTH_USER_MODEL = 'accounts.User'