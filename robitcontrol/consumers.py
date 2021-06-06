from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import Robit
import asyncio


@database_sync_to_async
def get_robit_by_key(key):
    return Robit.objects.get(key=key)

@database_sync_to_async
def bridge_from_robit(robit):
    return robit.update_bridge


class RobitSocketConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = None
        self.robit = None
        self.bridge = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"Robit{self.robit.id}",
            self.channel_name
        )
        await self.channel_layer.group_discard(
            f"Bridge{self.bridge.id}",
            self.channel_name
        )

    async def authenticate(self, message):
        self.key = message["key"]
        if len(self.key) < 64:
            await self.close(1008)
            return
        if self.robit is not None:
            await self.close(4001)
            return
        try:
            self.robit = await get_robit_by_key(self.key)
        except Robit.DoesNotExist:
            await self.close(4000)
            return
        await self.channel_layer.group_add(
            f"Robit{self.robit.id}",
            self.channel_name
        )
        self.bridge = await bridge_from_robit(self.robit)
        if self.bridge is not None:
            await self.channel_layer.group_add(
                f"Bridge{self.bridge.id}",
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        if message["type"] == "auth":
            await self.authenticate(message)
            return
        if message["type"] == "heartbeat":
            print(f"{self.robit.name}: Lub-Dub")
            return
        if self.robit is None:
            await self.close(4002)

    async def hook_event(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            "type": "update",
            'message': message
        }))

    async def command_event(self, event):
        command_map = {
            "forward": {"command": "motors", "left": 100, "right": 100},
            "left": {"command": "motors", "left": -100, "right": 100},
            "right": {"command": "motors", "left": 100, "right": -100},
            "backward": {"command": "motors", "left": -100, "right": -100},
            "stop": {"command": "motors", "left": 0, "right": 0}
        }

        payload = {
            "type": "command",
        }
        payload.update(command_map[event["command"]])
        await self.send(json.dumps(payload))


class BrowserSocketConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.user = None
        self.super_user = False

    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.super_user = self.user.is_superuser or False

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            message = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(json.dumps({
                "type": "error",
                "message": "Payload was not valid JSON"
            }))
            return
        if message["type"] == "command":
            await self.channel_layer.group_send(
                f"Robit{message['robit_id']}",
                {
                    "command": message["command"]
                }
            )
            await asyncio.sleep(0.5)
            await self.channel_layer.group_send(
                f"Robit{message['robit_id']}",
                {
                    "command": "stop"
                }
            )
