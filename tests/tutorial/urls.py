# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('tutorial.views',
    url(r'^$', 'index', name="tutorial_index"),
    url(r'^hello_world/$', 'hello_world', name="tutorial_hello_world"),
)
