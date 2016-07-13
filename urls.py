from django.conf.urls import url

from . import views

app_name = 'inventory'
urlpatterns = [
    # Non-generic, utility views.
    url(r'^$', views.index, name='index'),
    url(r'^host/details/(?P<host_id>[0-9]+)/$', views.load_host_details, name='load_host_details'),
    url(r'^load-table$', views.load_table, name='load_table'),
    # Generic List views.
    url(r'^bacula-cloud/$', views.BaculaCloudMemberListView.as_view(), name='bacula_member'),
    url(r'^host/$', views.HostListView.as_view(), name='host'),
    url(r'^jbod/$', views.JbodListView.as_view(), name='jbod'),
    url(r'^misc/$', views.MiscListView.as_view(), name='misc'),
    url(r'^pc/$', views.PCListView.as_view(), name='pc'),
    url(r'^physhost/$', views.PhysHostListView.as_view(), name='physhost'),
    url(r'^switch/$', views.SwitchListView.as_view(), name='switch'),
    url(r'^vmhost/$', views.VMHostListView.as_view(), name='vmhost'),
    url(r'^website/$', views.WebSiteListView.as_view(), name='website'),
    # Detail views.
    url(r'^physhost/details/(?P<pk>[0-9]+)/$', views.PhysHostDetailView.as_view(), name='physhost_details'),
    url(r'^vmhost/details/(?P<pk>[0-9]+)/$', views.VMHostDetailView.as_view(), name='vmhost_details'),
    url(r'^employee/details/(?P<pk>[0-9]+)/$', views.EmployeeDetailView.as_view(), name='employee_details'),
    url(r'^jbod/details/(?P<pk>[0-9]+)/$', views.JbodDetailView.as_view(), name='jbod_details'),
    url(r'^misc/details/(?P<pk>[0-9]+)/$', views.MiscDetailView.as_view(), name='misc_details'),
    url(r'^pc/details/(?P<pk>[0-9]+)/$', views.PCDetailView.as_view(), name='pc_details'),
    url(r'^switch/details/(?P<pk>[0-9]+)/$', views.SwitchDetailView.as_view(), name='switch_details'),
]
