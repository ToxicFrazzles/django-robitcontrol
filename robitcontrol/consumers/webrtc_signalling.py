from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ..models import Robit
from .utils import robit_connect_data, robit_disconnect, nop


class WebRTCConsumer(AsyncWebsocketConsumer):
    stream_token = None

    async def connect(self):
        self.stream_token = self.scope["url_route"]["kwargs"]["connection_token"]
        await self.channel_layer.group_add(
            f"webrtc{self.stream_token}",
            self.channel_name
        )
        await self.accept()
        # await self.channel_layer.group_send(
        #     f"webrtc{self.stream_token}",
        #     {
        #         "type": "webrtc.event",
        #         "text": '{"type": "info", "message": "Peer Connected"}',
        #         "sender": self.channel_name
        #     }
        # )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f"webrtc{self.stream_token}",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            f"webrtc{self.stream_token}",
            {
                "type": "webrtc.event",
                "text": text_data,
                "sender": self.channel_name
            }
        )

    async def webrtc_event(self, event):
        if event["sender"] == self.channel_name:
            return
        await self.send(text_data=event["text"])
