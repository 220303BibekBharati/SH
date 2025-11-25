from channels.generic.websocket import AsyncJsonWebsocketConsumer

class OrdersConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'orders'

    async def connect(self):
        user = self.scope.get('user')
        # Optionally restrict to staff: if not user.is_staff: await self.close(); return
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # Echo back or ignore; not needed for server push
        pass

    async def order_created(self, event):
        # Send event to client as JSON
        await self.send_json({
            'type': 'order_created',
            'order_id': event.get('order_id'),
            'user_id': event.get('user_id'),
            'total': str(event.get('total')),
            'created': event.get('created'),
        })
