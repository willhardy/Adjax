from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^basic/', include('basic.urls')),
)
