from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome!', #Email Subject
            'Thanks for creating account in to our website', #Email Message
            'aimodelverse@gmail.com',
            [instance.email],
            fail_silently=False,
        )

#
##
##

#