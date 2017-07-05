from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^gps_get_licen/$',views.gps_licen_input, name='gps_licen_input'),
    url('^driver_mobile_number/(?P<number>\w+)$', views.driver_mobile_number, name='driver_mobile_number'),
    url('^truck_mobile_number/(?P<number>\w+)$', views.truck_mobile_number, name='truck_mobile_number'),
    url('^print_form/$', views.print_form, name='print_form'),
    url('^upload_scaned_documents/$', views.upload_scaned_documents, name='upload_scaned_documents'),
    url('^mail_documents/$', views.mail_documents, name='mail_documents'),

    url('^tracking_device/$',views.tracking_device, name='tracking'),
    url('^display_lat_long/$', views.display_lat_long, name='display_lat_long'),
    url('^gps_lat_long/$', views.gps_lat_long, name="gps_lat_long")

]