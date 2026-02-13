from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import OrderStatusHistory
from orders.events import publish_event

@receiver(post_save, sender=OrderStatusHistory)
def order_status_changed(sender, instance, created, **kwargs):
    if created:
        publish_event(
            "order_status_changed",
            {
                "order_id": instance.order.id,
                "new_status": instance.new_status,  # ajuste aqui
                "changed_at": instance.changed_at.isoformat(),
            },
        )