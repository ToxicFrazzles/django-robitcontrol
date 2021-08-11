from django.db import models
from django.urls import reverse
import secrets
import webhooksocket.models


def random_ident():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(characters) for _ in range(64))


class Robit(models.Model):
    name = models.CharField(max_length=60)
    update_bridge = models.ForeignKey(
        webhooksocket.models.Bridge,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    key = models.CharField(
        max_length=64, unique=True,
        db_index=True, default=random_ident
    )
    available = models.BooleanField(default=False)
    channel_name = models.CharField(max_length=128, unique=True, null=True, default=None)

    def __str__(self):
        return self.name
