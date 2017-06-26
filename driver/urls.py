from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^add_driver_one/$', views.add_driver_one, name='add_driver_one'),
    url('^add_driver_one_process/$', views.add_driver_one_process, name='add_driver_one_process'),
    url('^add_driver_two/(\d+)$', views.add_driver_two, name='add_driver_two'),
    url('^add_driver_two_process/$', views.add_driver_two_process, name='add_driver_two_process'),
    url('^all_driver/$', views.all_driver, name='all_driver'),
    url('^driver_table/$', views.driver_table, name='driver_table'),
    url('^edit_driver/(\d+)$', views.edit_driver, name='edit_driver'),
    url('^edit_driver_two/(\d+)$', views.edit_driver_two, name='edit_driver_two'),
    url('^delete_driver/(\d+)$', views.delete_driver, name='delete_driver')

]
