from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Order


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        Notification.objects.create(
            user=customer,
            message=f"{customer.get_full_name()} ثبت سفارش کرد",
        )
