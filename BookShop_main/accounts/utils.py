from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def detectUrl(user):
    
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    


def send_verification_email(request, user, subject, email_template):
    
    from_email = 'Bookstore'
    current_site = get_current_site(request)
    mail_subject =subject
    message= render_to_string(
        email_template,
        {'user': user,
        'domain': current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        })
    to_mail = user.email
    mail = EmailMessage(mail_subject, message,from_email, to=[to_mail])
    mail.send()
    


def send_notification(mail_subject,mail_template, context):
    
    from_email = 'Bookstore'
    
    message= render_to_string(mail_template, context)
    if(isinstance(context['to_email'],str)):
        to_mail = []
        to_mail.append(context['to_email'])
    else:
        to_mail=context['to_email']
        
        
    mail = EmailMessage(mail_subject, message,from_email, to=to_mail)
    mail.send()