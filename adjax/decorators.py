#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__all__ = ('render_to_json')

from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson

from django.utils.functional import Promise 
from django.utils.encoding import force_unicode 

class LazyEncoder(json.DjangoJSONEncoder): 
    def default(self, obj): 
        if isinstance(obj, Promise): 
            return force_unicode(obj) 
        return obj 

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

from django.conf import settings
DEFAULT_REDIRECT = getattr(settings, 'ADJAX_DEFAULT_REDIRECT', None)

from django.shortcuts import redirect

def render_to_json(func):
    """ Renders the response using JSON, if appropriate.
    """
    def wrapper(request, *args, **kw):
        output = func(request, *args, **kw)
        if isinstance(output, dict):
            # Do not redirect AJAX calls
            if request.META.get('HTTP_X_REQUESTED_WITH', None) == 'XMLHttpRequest':
                # Remove request if given, we are using the one given in the input 
                output = output.copy()
                output.pop('request', None)
                return JsonResponse(output)

            referer = request.META.get('HTTP_REFERER', None)
            if referer:
                return redirect(referer)

            # TODO: Convert this to try ... except
            if DEFAULT_REDIRECT:
                return redirect(DEFAULT_REDIRECT)
            else:
                return HttpResponse()
        return output
    return wrapper
