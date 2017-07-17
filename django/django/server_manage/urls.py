from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from views import  *

urlpatterns = patterns('',
    url(r'^$',login),
    url(r'^login/',login),
    url(r'index/',index),
    url(r'start/',start),
    url(r'create/',create),
    url(r'logout/',logout),
    url(r'eventsource/',eventsource),




)


