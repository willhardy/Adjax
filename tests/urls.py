from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^demo/', include('basic.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
