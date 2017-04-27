from django.contrib import admin
from .models import *

from django.utils.text import capfirst
from django.utils.datastructures import OrderedDict

# 让model在admin中按注册顺序显示
def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse

    return inner

registry = OrderedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)
###########################################################################################
# Register your models here.


class SubPortInline(admin.TabularInline):
    model = SubPort
    extra = 0


class PortInline(admin.TabularInline):
    model = Port
    extra = 0
    inlines = [SubPortInline]
    fields = ('name', 'ip', 'mask', 'is_sub_port', 'father_port', 'is_mgmt_port', 'changeform_link')
    readonly_fields = ('changeform_link',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    inlines = [PortInline]
    list_display = ['hostname', 'vendor_model', 'auth_profile', 'snmp_community']
    list_filter = ['vendor_model__vendor__name', 'vendor_model__name']
    search_fields = ['vendor_model__vendor__name', 'vendor_model__name', 'hostname']
    empty_value_display = '-empty-'


@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    inlines = [SubPortInline]
    list_display = ['device', 'name', 'ip', 'mask', 'is_sub_port', 'father_port', 'is_mgmt_port', ]
    list_display_links = ['name']
    list_filter = ['device']
    search_fields = ['device__hostname']
    empty_value_display = '-empty-'

#admin.site.register(Device, DeviceAdmin)
#admin.site.register(Port, PortAdmin)
#admin.site.register(SubPort)
#admin.site.register(Vendor)
#admin.site.register(VendorModel)
#admin.site.register(AuthProfile)
#admin.site.register(SnmpCommunity)
@admin.register(Task)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    pass


@admin.register(VendorModel)
class VendorModelAdmin(admin.ModelAdmin):
    pass


@admin.register(AuthProfile)
class AuthProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(SnmpCommunity)
class SnmpCommunityAdmin(admin.ModelAdmin):
    pass


