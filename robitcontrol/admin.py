from django.contrib import admin
from .models import Robit, WebRTCBrowser


class RobitAdmin(admin.ModelAdmin):
    fields = ('name', 'update_bridge', 'key', 'available', "channel_name")
    readonly_fields = ('key', "channel_name")


class WebRTCBrowserAdmin(admin.ModelAdmin):
    fields = ('name', 'token', 'key', 'url')
    readonly_fields = ('token', 'key', 'url')


admin.site.register(WebRTCBrowser, WebRTCBrowserAdmin)
admin.site.register(Robit, RobitAdmin)
