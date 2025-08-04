from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification

@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.customer,
            message=f"سفارش جدید توسط {instance.customer.get_full_name()} ثبت شد."
        )
