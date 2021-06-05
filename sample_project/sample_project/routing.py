from django.urls import path, include
from channels.routing import URLRouter
import robitcontrol.routing


websocket_urlpatterns = [
    path('robitcontrol/', URLRouter(robitcontrol.routing.websocket_urlpatterns), name='robitcontrol')
]
