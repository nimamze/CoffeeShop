from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Order


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        full_name = customer.get_full_name() or customer.username
        Notification.objects.create(
            user=customer,
            message=f"سفارش جدید توسط {full_name} ثبت شد.",
        )
