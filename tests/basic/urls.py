#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('tests.basic.views',
    url(r'^replace/$', 'replace', name="replace"),
    url(r'^hide/$', 'hide', name="hide"),
    url(r'^messages/$', 'messages', name="messages"),
    url(r'^update/$', 'update',  name="update"),
    url(r'^forms/$', 'forms',  name="forms"),
    url(r'^redirect/$', 'redirect',  name="redirect"),
    url(r'^django_redirect/$', 'django_redirect',  name="django_redirect"),
    url(r'^extra/$', 'extra',  name="extra"),
    url(r'^extra_2/$', 'extra_2',  name="extra_2"),
    url(r'^do_everything/$', 'do_everything',  name="do_everything"),
    url(r'^do_nothing/$', 'do_nothing',  name="do_nothing"),
    url(r'^$', 'demo',  name="demo"),
)
