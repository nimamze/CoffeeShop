from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, CartItem

@receiver(post_save, sender=CartItem)
def cart_created_handler(sender, instance, created, **kwargs):
    if created:
        customer = instance.cart.customer 
        Notification.objects.create(
            user=customer,
            message=f"{customer.get_full_name()} محصول '{instance.product.name}' را به سبد خرید اضافه کرد."
        )
