# -*- coding: UTF-8 -*-

__all__ = ('adjax_response',)

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.conf import settings

from django.core.serializers import json, serialize

from adjax.base import get_store
from django.utils.functional import Promise 
from django.utils.encoding import force_unicode 

class LazyEncoder(json.DjangoJSONEncoder): 
    def default(self, obj): 
        if isinstance(obj, Promise): 
            return force_unicode(obj) 
        return super(LazyEncoder, self).default(obj)

class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(
                object, indent=2, cls=LazyEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')

# Where to redirect to when view is called without an ajax request.
DEFAULT_REDIRECT = getattr(settings, 'ADJAX_DEFAULT_REDIRECT', None)
ADJAX_CONTEXT_KEY = 'adjax'


def adjax_response(func):
    """ Renders the response using JSON, if appropriate.
    """
    # TODO allow a template to be given for non-ajax requests
    template_name = None

    def wrapper(request, *args, **kw):
        output = func(request, *args, **kw)
        store = get_store(request)

        # If a dict is given, add that to the output
        if output is None:
            output = {}
        elif isinstance(output, dict):
            output = output.copy()
            output.pop('request', None)
            for key, val in output.items():
                store.extra(key, val)

        # Intercept redirects
        elif isinstance(output, HttpResponse) and output.status_code in (301, 302):
            store.redirect(output['Location'])

        if request.is_ajax():
            return store.json_response

        if isinstance(output, dict):
            # If we have a template, render that
            if template_name:
                output.setdefault(ADJAX_CONTEXT_KEY, store)
                return render_to_response(template_name, output, context_instance=RequestContext(request))

            # Try and redirect somewhere useful
            if 'HTTP_REFERER' in request.META:
                return redirect(request.META['HTTP_REFERER'])
            elif DEFAULT_REDIRECT:
                return redirect(DEFAULT_REDIRECT)
            else:
                return HttpResponse()

        return output

    return wrapper
