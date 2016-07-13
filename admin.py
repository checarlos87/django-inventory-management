from django.contrib import admin

from .models import *

# Register your models here.

class NetifaceInline(admin.StackedInline):
    model = Netiface

class HostAdmin(admin.ModelAdmin):
    inlines = [NetifaceInline]
    filter_horizontal = ['services']
    list_display = (
        'name', 
        'get_netiface_ip', 
        'is_bacula_fd', 
        'is_ansible_managed',
    )

class PhysHostAdmin(HostAdmin):
    pass

class VMHostAdmin(HostAdmin):
    fields = [
        'name', 
        'description', 
        'services', 
        'os', 
        'is_bacula_fd', 
        'is_ansible_managed', 
        'host_machine'
    ]

class PCAdmin(admin.ModelAdmin):
    pass
#    fields = ['name', 'property_num', 'description', 'brand', 'series', 'model', 'custodial']

class SwitchAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'ip',
        'building',
    ]

class CloudMemberAdmin(admin.ModelAdmin):
    list_display = [
        'get_member_name',
        'role',
    ]

class WebSiteAdmin(admin.ModelAdmin):
    list_display = ['fqdn', 'get_webhost_name', 'get_webhost_ip']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 
        'email',
        'ext',
    ]

class JbodAdmin(admin.ModelAdmin):
    filter_horizontal = ['managers']

admin.site.register(PhysHost, PhysHostAdmin)
admin.site.register(VMHost, VMHostAdmin)
admin.site.register(Switch, SwitchAdmin)
admin.site.register(Jbod, JbodAdmin)
admin.site.register(PC, PCAdmin)
admin.site.register(Misc)
admin.site.register(MiscType)
admin.site.register(BaculaCloudMember, CloudMemberAdmin)
admin.site.register(WebSite, WebSiteAdmin)
admin.site.register(Service)
admin.site.register(HostOS)
admin.site.register(SwitchOS)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Building)
