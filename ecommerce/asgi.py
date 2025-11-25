import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

django_asgi_app = get_asgi_application()

try:
    import ecommerce.routing  # noqa: F401
except Exception:
    ecommerce_routing = None
else:
    from ecommerce.routing import websocket_urlpatterns as project_ws_patterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(project_ws_patterns if 'project_ws_patterns' in globals() else [])
    ),
})
