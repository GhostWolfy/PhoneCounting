from django.contrib import admin
from .models import *


# class DeviceAdmin(admin.ModelAdmin):

admin.site.register(Device)
admin.site.register(DeviceReal)
admin.site.register(DeviceModem)
admin.site.register(Company)
admin.site.register(Object)
admin.site.register(SIMCard)
admin.site.register(LavinaObject)
admin.site.register(LavinaDevice)