from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from server_manage.views import *

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^view/', include('server_view.urls')),
    url(r'^',include('server_manage.urls')),


)
