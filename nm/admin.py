from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Device)
admin.site.register(AuthProfile)
admin.site.register(Port)
admin.site.register(SubPort)
admin.site.register(Vendor)
admin.site.register(VendorModel)
admin.site.register(SnmpCommunity)
