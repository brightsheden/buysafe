from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import  User
from .models import Profile,Balance
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != "":
        user.username = user.email
pre_save.connect(updateUser, sender=User)

def generate_passcode():
    return get_random_string(length=6, allowed_chars='0123456789')

def profile(sender,instance,created,**kwargs):
    passcode = generate_passcode()  # Generate a passcode
    if created:
        profile =Profile.objects.create(
            user = instance,
            email = instance.email,
            name = instance.username,
            email_verified=False,  # User is not active until email confirmation
            passcode=passcode,  # Save the passcode with the user
    
        )

        Balance.objects.create(
            profile =profile
        )



        email_subject = 'Email Confirmation Passcode'
        email_message = f'Your passcode for email confirmation: {passcode}'
        from_email = 'shedenbright@gmail.com'  # Change to your email address
        recipient_list = [instance.email]
        send_mail(email_subject, email_message, from_email, recipient_list, fail_silently=False)
  

post_save.connect(profile, sender=User)

