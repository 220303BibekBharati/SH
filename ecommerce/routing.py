from django.urls import path
from orders.routing import websocket_urlpatterns as orders_ws_patterns

# Aggregate websocket URL patterns from apps
websocket_urlpatterns = [
    *orders_ws_patterns,
]
