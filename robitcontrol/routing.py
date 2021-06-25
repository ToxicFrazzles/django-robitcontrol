from django.urls import path, re_path, register_converter
from . import views
from . import consumers

app_name = "robitcontrol"


urlpatterns = [
    path('robitsocket/', consumers.RobitSocketConsumer.as_asgi(), name='robitsocket'),
    path('browsersocket/', consumers.BrowserSocketConsumer.as_asgi(), name='browsersocket'),
    re_path(r"webrtcsignal/(?P<connection_token>[\w]*)/", consumers.WebRTCConsumer.as_asgi(), name='webrtc')
]
websocket_urlpatterns = urlpatterns
