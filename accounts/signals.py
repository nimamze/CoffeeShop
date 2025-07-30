from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            subject='Welcome to our website!',
            message=f'Hi {instance.first_name},\n\nThank you for registering on our site. Welcome aboard!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
