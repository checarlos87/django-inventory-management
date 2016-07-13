from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from .models import *

# Redirect to appropriate view based on drop-down
# main menu selection.
def load_table(request):
    if request.POST:
        table_name = request.POST['db-table']
        return redirect('/inventory/' + table_name)

    else:
        return redirect('/')

# Resolve the polymorphism of Host as either a PhysHost or a VMHost
# and return the appropriate view.
def load_host_details(request, host_id):
    host = Host.objects.get(id = host_id)
    try:
        phys = host.physhost
        return HttpResponseRedirect(reverse('inventory:physhost_details', args=(phys.id,)))
    except(Host.DoesNotExist):
        vm = host.vmhost
        return HttpResponseRedirect(reverse('inventory:vmhost_details', args=(vm.id,)))

def troglodita_seal(request):
    return render(request, 'inventory/troglodita.html')

def index(request):
    return render(request, 'inventory/index.html')

##### Generic List Views #####

###  Hosts  ###

# All Hosts
class HostListView(generic.ListView):
    template_name = 'inventory/host_list.html'
    context_object_name = 'host_list'
    extra_context = {
        'bacula_fd_count': len(Host.objects.filter(is_bacula_fd = True)),
        'ansible_managed_count': len(Host.objects.filter(is_ansible_managed = True))
    }

    def get_context_data(self, **kwargs):
        context = super(HostListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get_queryset(self):
        return Host.objects.order_by('name')

# Physical Hosts
class PhysHostListView(generic.ListView):
    template_name = 'inventory/physhost_list.html'
    context_object_name = 'host_list'
    extra_context = { 
        'bacula_fd_count': len(PhysHost.objects.filter(is_bacula_fd = True)),
        'ansible_managed_count': len(PhysHost.objects.filter(is_ansible_managed = True))
    }   

    def get_context_data(self, **kwargs):
        context = super(PhysHostListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


    def get_queryset(self):
        return PhysHost.objects.order_by('name')

# VM Hosts
class VMHostListView(generic.ListView):
    template_name = 'inventory/vmhost_list.html'
    context_object_name = 'host_list'
    extra_context = { 
        'bacula_fd_count': len(VMHost.objects.filter(is_bacula_fd = True)),
        'ansible_managed_count': len(VMHost.objects.filter(is_ansible_managed = True))
    }   

    def get_context_data(self, **kwargs):
        context = super(VMHostListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get_queryset(self):
        return VMHost.objects.order_by('name')

### Cloud Member Tables ###

# Bacula Member
class BaculaCloudMemberListView(generic.ListView):
    template_name = 'inventory/bacula_member_list.html'
    context_object_name = 'member_list'
    extra_context = {
        'sd_count': len(BaculaCloudMember.objects.filter(role = 'SD')),
        'dir_count': len(BaculaCloudMember.objects.filter(role = 'DIR')),
    }

    def get_context_data(self, **kwargs):
        context = super(BaculaCloudMemberListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get_queryset(self):
        return BaculaCloudMember.objects.all()

### Other equipment ###

# Switches
class SwitchListView(generic.ListView):
    template_name = 'inventory/switch_list.html'
    context_object_name = 'switch_list'
    extra_context = {
        'eth_count': len(Switch.objects.filter(switch_type = 'ETH')),
        'ib_count': len(Switch.objects.filter(switch_type = 'IB')),
    }

    def get_context_data(self, **kwargs):
        context = super(SwitchListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get_queryset(self):
        return Switch.objects.order_by('id')

# PCs
class PCListView(generic.ListView):
    template_name = 'inventory/pc_list.html'
    context_object_name = 'pc_list'
    extra_context = {
        'assigned_count': len(PC.objects.filter(~Q(custodial = None))),
    }

    def get_context_data(self, **kwargs):
        context = super(PCListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get_queryset(self):
        return PC.objects.order_by('id')

# Jbod
class JbodListView(generic.ListView):
    template_name = 'inventory/jbod_list.html'
    context_object_name = 'jbod_list'

    def get_queryset(self):
        return Jbod.objects.order_by('name')

# Misc
class MiscListView(generic.ListView):
    template_name = 'inventory/misc_list.html'
    context_object_name = 'misc_list'

    def get_queryset(self):
        return Misc.objects.order_by('name')

# WebSite
class WebSiteListView(generic.ListView):
    template_name = 'inventory/website_list.html'
    context_object_name = 'website_list'

    def get_queryset(self):
        return WebSite.objects.order_by('fqdn')

##### Generic Detail veiws ######

# Physical Hosts
class PhysHostDetailView(generic.DetailView):
    model = PhysHost
    template_name = 'inventory/physhost_detail.html'

# VM Hosts
class VMHostDetailView(generic.DetailView):
    model = VMHost
    template_name = 'inventory/vmhost_detail.html'

# JBODs
class JbodDetailView(generic.DetailView):
    model = Jbod
    template_name = 'inventory/jbod_detail.html'

# Misc
class MiscDetailView(generic.DetailView):
    model = Misc
    template_name = 'inventory/misc_detail.html'

# Switches
class SwitchDetailView(generic.DetailView):
    model = Switch
    template_name = 'inventory/switch_detail.html'

# PCs
class PCDetailView(generic.DetailView):
    model = PC
    template_name = 'inventory/pc_detail.html'

# Employees
class EmployeeDetailView(generic.DetailView):
    model = Employee
    template_name = 'inventory/employee_detail.html'

