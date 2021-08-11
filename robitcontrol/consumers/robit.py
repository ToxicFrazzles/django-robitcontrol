from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ..models import Robit
from .utils import robit_connect_data, robit_disconnect, nop


class RobitSocketConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = None
        self.robit = None
        self.bridge_group = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.bridge_group is not None:
            await self.channel_layer.group_discard(
                self.bridge_group,
                self.channel_name
            )
        await self.channel_layer.group_send(
            f"RobotBrowser",
            {
                "type": "robot.unavailable",
                "cause": "connection",
                "robot": {
                    "ID": self.robit.id,
                    "name": self.robit.name
                }
            }
        )
        await robit_disconnect(self.robit["id"])

    async def authenticate(self, message):
        await self.send(text_data='{"type": "info", "message": "Authentication started", "payload": "' + str(message) + '"}')
        self.key = message["key"]
        await self.send(text_data='{"type": "info", "message": "Uno"}')
        if len(self.key) < 64:
            await self.close(1008)
            return
        await self.send(text_data='{"type": "info", "message": "Dos"}')
        if self.robit is not None:
            await self.close(4001)
            return
        await self.send(text_data='{"type": "info", "message": "Three"}')
        try:
            connect_data = await robit_connect_data(self.key, self.channel_name)
            await self.send(text_data=json.dumps(connect_data))
            self.robit = connect_data["robit"]
            self.bridge_group = connect_data["bridge_group"]
        except Robit.DoesNotExist:
            await self.close(4000)
            return
        except Exception as e:
            await self.send(text_data="SHIT'S FUCKED M8!")
            await self.send(text_data=str(e))
            await self.close()
            return
        await self.send(text_data='{"type": "info", "message": "Four"}')
        if self.bridge_group is not None:
            await self.channel_layer.group_add(
                self.bridge_group,
                self.channel_name
            )
        await self.send(text_data='{"type": "info", "message": "Five"}')
        await self.channel_layer.group_send(
            f"RobotBrowser",
            {
                "type": "robot.available",
                "cause": "connection",
                "robot": {
                    "ID": self.robit.id,
                    "name": self.robit.name
                }
            }
        )
        await self.send(text_data='{"type": "info", "message": "Authenticated"}')

    async def receive(self, text_data=None, bytes_data=None):
        try:
            message = json.loads(text_data)
        except json.JSONDecodeError:
            return      # Just silently ignore non-JSON data

        if message["type"] == "auth":
            await self.authenticate(message)
            return
        if message["type"] == "heartbeat":
            return
        if self.robit is None:
            await self.close(4002)

    async def hook_event(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            "type": "update",
            'message': message
        }))

    async def motor_command(self, event):
        command_map = {
            "forward": {"left": 255, "right": 255},
            "left": {"left": -255, "right": 255},
            "right": {"left": 255, "right": -255},
            "backward": {"left": -255, "right": -255},
            "stop": {"left": 0, "right": 0}
        }

        payload = {
            "type": "command",
            "command": "motors"
        }
        payload.update(command_map[event["command"]])
        await self.send(json.dumps(payload))

    async def shutdown_command(self, event):
        await self.send(json.dumps({
            "type": "command",
            "command": "shutdown"
        }))
