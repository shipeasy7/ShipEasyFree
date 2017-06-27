from django.conf.urls import url,include
from . import views
urlpatterns = [
    url('^pair/$', views.truck_driver_pair, name="pair"),
    url('^pair_process/$',views.pair_process, name='pair_process'),
    url('^status_table/$', views.status_table, name="status_table"),
    url('^status_table_data/$', views.status_table_data, name="status_table_data"),
]