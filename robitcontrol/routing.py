from django.urls import path, register_converter
from . import views
from . import consumers

app_name = "robitcontrol"


urlpatterns = [
    path('robitsocket/', consumers.RobitSocketConsumer.as_asgi(), name='robitsocket'),
    path('browsersocket/', consumers.BrowserSocketConsumer.as_asgi(), name='browsersocket')
]
websocket_urlpatterns = urlpatterns
