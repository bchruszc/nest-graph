from django.contrib import admin
from models import DeviceState, Device, UserProfile

class DeviceAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

class DeviceStateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceState, DeviceStateAdmin)
admin.site.register(UserProfile, UserProfileAdmin)