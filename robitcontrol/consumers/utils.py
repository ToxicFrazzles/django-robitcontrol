from channels.db import database_sync_to_async
from ..models import Robit, WebRTCBrowser


@database_sync_to_async
def get_robit_by_id(robot_id):
    robit = Robit.objects.get(id=robot_id)
    return {
        "group": f"Robit{robit.id}",
        "id": robit.id,
        "name": robit.name,
        "available": robit.available,
        "channel": robit.channel_name
    }


@database_sync_to_async
def get_robit_by_key(key):
    try:
        return Robit.objects.get(key=key)
    except Robit.DoesNotExist:
        return None


@database_sync_to_async
def robit_connect_data(key, channel_name):
    robit = Robit.objects.get(key=key)
    robit.channel_name = channel_name
    robit.save()
    bridge = robit.update_bridge
    return {
        "robit": {
            "group": f"Robit{robit.id}",
            "id": robit.id,
            "name": robit.name,
            "available": robit.available,
            "channel": channel_name
        },
        "bridge_group": f"Bridge{bridge.id}"
    }


@database_sync_to_async
def robit_disconnect(robit_id):
    robit = Robit.objects.get(id=robit_id)
    robit.channel_name = None
    robit.save()


@database_sync_to_async
def get_webrtc_browser(token, key):
    try:
        return WebRTCBrowser.objects.get(token=token, key=key)
    except WebRTCBrowser.DoesNotExist:
        return None


async def nop(*args, **kwargs):
    return
