from channels.generic.websocket import AsyncWebsocketConsumer
import json
from typing import Dict
from .utils import get_robit_by_id
from django.core.exceptions import ObjectDoesNotExist


class BrowserSocketConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.user = None
        self.super_user = False
        self.current_robot = None

    async def connect(self):
        await self.channel_layer.group_add(
            f"RobotBrowser",
            self.channel_name
        )
        await self.accept()
        self.user = self.scope["user"]
        self.super_user = self.user.is_superuser or False
        if self.user.is_staff:
            await self.channel_layer.group_add(
                f"RobotStaff",
                self.channel_name
            )
        else:
            await self.channel_layer.group_add(
                f"RobotNonStaff",
                self.channel_name
            )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f"RobotBrowser",
            self.channel_name
        )
        if self.user.is_staff:
            await self.channel_layer.group_discard(
                f"RobotStaff",
                self.channel_name
            )
        else:
            await self.channel_layer.group_discard(
                f"RobotNonStaff",
                self.channel_name
            )
        if self.current_robot is not None:
            await self.channel_layer.group_discard(
                self.current_robot["group"],
                self.channel_name
            )

    async def select_robot(self, message: Dict):
        try:
            robit = await get_robit_by_id(message["id"])
        except ObjectDoesNotExist:
            await self.send(json.dumps({
                "type": "error",
                "message": "robot with given ID is not online"
            }))
            return
        if not robit["available"] and not self.user.is_staff:
            await self.send(json.dumps({
                "type": "error",
                "message": "robot with given ID is not online"
            }))
            return
        if self.current_robot is not None:
            await self.channel_layer.group_discard(
                self.current_robot["group"],
                self.channel_name
            )
        self.current_robot = robit
        await self.channel_layer.group_add(
            self.current_robot["group"],
            self.channel_name
        )
        await self.send(text_data='{"type": "info", "message": "Selected robot"}')

    async def process_command(self, message: Dict):
        if self.current_robot is None:
            await self.send(json.dumps({
                "type": "error",
                "message": "You need to select a robot first"
            }))
            return
        if message["command"] == "shutdown" and self.super_user:
            await self.channel_layer.group_send(
                self.current_robot["group"],
                {
                    "type": "shutdown.command",
                }
            )
        else:
            await self.channel_layer.group_send(
                self.current_robot["group"],
                {
                    "type": "motor.command",
                    "command": message["command"]
                }
            )

    async def process_config(self, message: Dict):
        if message["option"] == "enable" and self.user.is_staff:
            await self.channel_layer.group_send(
                f"RobotBrowser",
                {
                    "type": ("robot.available" if message["value"] else "robot.unavailable"),
                    "cause": "toggle",
                    "robot": {
                        "ID": message["robit_id"],
                        "name": (await get_robit_by_id(message["robit_id"])).name
                    }
                }
            )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            message: Dict = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(json.dumps({
                "type": "error",
                "message": "Payload was not valid JSON"
            }))
            return

        handler_map = {
            "command": self.process_command,
            "config": self.process_config,
            "select": self.select_robot
        }
        await handler_map[message["type"]](message)

    async def robot_available(self, event):
        await self.send(json.dumps({
            "type": "robot_available",
            "cause": event["cause"] if self.user.is_staff else "connection",
            "robot": event["robot"]
        }))

    async def robot_unavailable(self, event):
        await self.send(json.dumps({
            "type": "robot_unavailable",
            "cause": event["cause"] if self.user.is_staff else "connection",
            "robot": event["robot"]
        }))
