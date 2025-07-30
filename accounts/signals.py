from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Welcome to our website!',
            message='Hi {}, thank you for registering on our site. be site ma khosh Amadid.'.format(instance.username),
            from_email=None,
            recipient_list=[instance.email],
            fail_silently=False,
        )
