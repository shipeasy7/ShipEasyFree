from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^add_truck_one/$', views.add_truck_one, name='add_truck_one'),
    url('^add_truck_one_process/$', views.add_truck_one_process, name='add_truck_one_process'),
    url('^add_truck_two/(\d+)$', views.add_truck_two, name='add_truck_two'),
    url('^add_truck_two_process/$', views.add_truck_two_process, name='add_truck_two_process'),
    url('^add_truck_three/(\d+)$', views.add_truck_three, name='add_truck_three'),
    url('^add_truck_three_process/$', views.add_truck_three_process, name='add_truck_three_process'),
    url('^truck_table/$', views.truck_table, name='truck_table'),
    url('^all_truck/$', views.all_truck, name='all_truck'),
    url('^edit_truck/(\d+)$', views.edit_truck, name='edit_truck'),
    url('^edit_truck_two/(\d+)$', views.edit_truck_two, name='edit_truck_two'),
    url('^edit_truck_three/(\d+)$', views.edit_truck_three, name='edit_truck_three'),
    url('^deleate_truck/(\d+)', views.delete_truck, name="deleate_truck"),

]