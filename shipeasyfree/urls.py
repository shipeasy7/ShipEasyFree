"""shipeasyfree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from base import views

from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'session_security/', include('session_security.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^$', include('base.urls')),
    url(r'^admin/', admin.site.urls),
    url('^base/',include('base.urls')),

    url('^truck/', include('truck.urls')),
    url('^driver/', include('driver.urls')),
    url('^gps/', include('gps.urls')),
    # url('^truck_driver_pair/', include('truckDriverPair.urls')),
    url('^truck_driver_pair/', include('truckDriverPair.urls')),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
