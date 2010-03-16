from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/what/'}, name="home"),
    url(r'^what/$', 'direct_to_template', {'template': 'what.html', 'extra_context': {'page': 'what'}}, name="what"),
    url(r'^how/$', 'direct_to_template', {'template': 'how.html', 'extra_context': {'page': 'how'}}, name="how"),
    url(r'^where/$', 'direct_to_template', {'template': 'where.html', 'extra_context': {'page': 'where'}}, name="where"),
    url(r'^who/$', 'direct_to_template', {'template': 'who.html', 'extra_context': {'page': 'who'}}, name="who"),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )

