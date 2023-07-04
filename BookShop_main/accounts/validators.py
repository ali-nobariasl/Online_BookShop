from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    exp = os.path.splitext(value.name)[1]      # ali.jpg 
    print(exp)
    valid_extensions = ['jpg', 'jpeg', 'png']
    
    if not exp.lower() in valid_extensions:
        raise ValidationError('unsupported extension. Allowed extensions:'+ str(valid_extensions))
        
    