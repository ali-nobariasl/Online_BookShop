from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import User, UserProfile



# sender,instance,created, **kwargs
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    
    if created:
        UserProfile.objects.create(user=instance)
        print("user is created")
        
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("profile is updated")
        except:
            profile = UserProfile.objects.create(user=instance) 
            print("profile was not exists, but was created")
            
            
            
post_save.connect(post_save_create_profile_receiver, sender=User)