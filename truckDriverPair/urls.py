from django.conf.urls import url,include
from . import views
urlpatterns = [
    url('^pair/$', views.truck_driver_pair, name="pair"),
    url('^pair_process/$',views.pair_process, name='pair_process'),
    url('^status_table/$', views.status_table, name="status_table"),
    url('^status_table_data/$', views.status_table_data, name="status_table_data"),
    url('^status_change/(\d+)$', views.status_change, name="status_change"),
    url('^status_change_process/$', views.status_change_process, name="status_change_process"),
    url('^unpair_status/$', views.unpair_status, name="unpair_status"),
    url('^unpair_status_process/$', views.unpair_status_process, name="unpair_status_process"),
    url('find_driver_name/(?P<licanse_numbers>\w+)', views.licen_through_driver_name, name="find_driver_name"),
    url('find_truck_licen/(?P<driver_name>\w+)', views.find_licen_from_driver, name="driver_name"),

]