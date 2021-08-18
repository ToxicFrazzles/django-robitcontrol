from django.db import models
from django.urls import reverse
from django.templatetags.static import static
import secrets
import webhooksocket.models


TOKEN_LENGTH = 16
KEY_LENGTH = 64


def generate_token(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(characters) for _ in range(length))


def random_token():
    return generate_token(TOKEN_LENGTH)


def random_key():
    return generate_token(KEY_LENGTH)


class Robit(models.Model):
    name = models.CharField(max_length=60)
    update_bridge = models.ForeignKey(
        webhooksocket.models.Bridge,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    key = models.CharField(
        max_length=KEY_LENGTH, unique=True,
        db_index=True, default=random_key
    )
    available = models.BooleanField(default=False)
    channel_name = models.CharField(max_length=128, unique=True, null=True, default=None)

    def __str__(self):
        return self.name


class WebRTCBrowser(models.Model):
    name = models.CharField(max_length=60)
    token = models.CharField(max_length=TOKEN_LENGTH, default=random_token, unique=True, db_index=True)
    key = models.CharField(max_length=KEY_LENGTH, default=random_key)

    def __str__(self):
        return f"{self.name}"

    @property
    def url(self):
        return static("webrtc.html") + f"?t=<TOKEN>&bt={self.token}&bk={self.key}"

