from django.urls import path, include
from channels.routing import URLRouter
import webhooksocket.routing
import robitcontrol.routing


websocket_urlpatterns = [
    path('robitcontrol/', URLRouter(robitcontrol.routing.websocket_urlpatterns), name='robitcontrol'),
    path('whs/', URLRouter(webhooksocket.routing.websocket_urlpatterns), name='sockets')
]
