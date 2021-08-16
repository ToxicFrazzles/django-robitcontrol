from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ..models import Robit
from .utils import robit_connect_data, robit_disconnect, nop, get_robit_by_key, get_webrtc_browser


class WebRTCConsumer(AsyncWebsocketConsumer):
    stream_token = None
    authenticated = False

    async def connect(self):
        self.stream_token = self.scope["url_route"]["kwargs"]["connection_token"]
        await self.channel_layer.group_add(
            f"webrtc{self.stream_token}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f"webrtc{self.stream_token}",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        message_obj = json.loads(text_data)
        if message_obj["type"] == "auth_robit":
            await self.authenticate_robit(message_obj)
        elif message_obj["type"] == "auth_browser":
            await self.authenticate_browser(message_obj)
        elif not self.authenticated:
            await self.close(4000)
        else:
            await self.channel_layer.group_send(
                f"webrtc{self.stream_token}",
                {
                    "type": "webrtc.event",
                    "text": text_data,
                    "sender": self.channel_name
                }
            )

    async def authenticate_robit(self, message):
        if get_robit_by_key(message["key"]) is not None:
            self.authenticated = True
        else:
            await self.close(4000)

    async def authenticate_browser(self, message):
        try:
            token = message["token"]
            key = message["key"]
        except KeyError:
            await self.close(1002)
            return
        if get_webrtc_browser(token, key) is not None:
            self.authenticated = True
        else:
            await self.close(4000)

    async def webrtc_event(self, event):
        if not self.authenticated:
            return
        if event["sender"] == self.channel_name:
            return
        await self.send(text_data=event["text"])
