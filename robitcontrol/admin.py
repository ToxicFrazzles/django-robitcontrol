from django.contrib import admin
from .models import Robit


class RobitAdmin(admin.ModelAdmin):
    fields = ('name', 'update_bridge', 'key', 'available', "channel_name")
    readonly_fields = ('key', "channel_name")


admin.site.register(Robit, RobitAdmin)
