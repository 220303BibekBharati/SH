from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def broadcast_order_created(sender, instance: Order, created, **kwargs):
    if not created:
        return
    channel_layer = get_channel_layer()
    total = instance.get_total_cost()
    payload = {
        'type': 'order_created',  # maps to OrdersConsumer.order_created
        'order_id': instance.id,
        'user_id': instance.user_id,
        'total': total,
        'created': instance.created.isoformat(),
    }
    async_to_sync(channel_layer.group_send)('orders', payload)
