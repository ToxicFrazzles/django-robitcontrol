from django.contrib import admin
from .models import Robit


class RobitAdmin(admin.ModelAdmin):
    fields = ('name', 'update_bridge', 'key')
    readonly_fields = ('key',)


admin.site.register(Robit, RobitAdmin)
