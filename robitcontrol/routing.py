from django.urls import path, register_converter
from . import views
from . import consumers

app_name = "robitcontrol"


websocket_urlpatterns = [
    path('robitsocket', consumers.SocketConsumer.as_asgi(), name='robitsocket')
]
