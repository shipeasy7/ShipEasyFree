from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^register/$', views.register, name='register'),
    url('^registration_process/$', views.registration_process, name='registration_process'),
    url('^activete_user/(\d+)/$', views.activete_user, name='activete_user'),
    url('^login/$', views.login, name='login'),
    url('^login_process/$', views.login_process, name='login_process'),
    url('^base/$', views.base, name='base'),
    url('^profile/$', views.profile, name='profile'),
    url('^edit_profile_one/$', views.edit_profile_one, name='edit_profile'),
    url('^edit_profile_one_process/$', views.edit_profile_one_process, name='edit_profile_one'),
    url('^edit_profile_two/$', views.edit_profile_two, name='edit_profile_two'),
    url('^edit_profile_two_process/$', views.edit_profile_two_process, name='edit_profile_two_process'),
    url('^edit_profile_three/$', views.edit_profile_three, name='edit_profile_three'),
    url('^edit_profile_three_process/$', views.edit_profile_three_process, name='edit_profile_three_process'),

]