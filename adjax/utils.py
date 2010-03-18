#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.core.serializers import json, serialize
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.contrib import messages
from django.core import urlresolvers

def get_store(request):
    """ Gets a relevant store object from the given request. """
    if not hasattr(request, '_adjax_store'):
        request._adjax_store = AdjaxStore(request)
    return request._adjax_store


def get_key(instance, field_name):
    """ Returns the key that will be used to identify dynamic fields in the DOM. """
    # TODO: Avoid any characters that may not appear in class names
    m = instance._meta
    return '-'.join(('data', m.app_label, m.object_name, str(instance.pk), field_name))


class AdjaxStore(object):
    """ This class will help store ajax data collected in views. """

    def __init__(self, request):
        self.request = request
        self.update_data = {}
        self.form_data = {}
        self.replace_data = {}
        self.hide_data = []
        self.extra_data = {}
        self.redirect_data = None

    @property
    def messages_data(self):
        return [{'tags': m.tags, 'content': unicode(m)} for m in messages.get_messages(self.request)]

    def update(self, obj, attributes=None):
        """ Make values from a given object available. """
        for attr in attributes:
            value = getattr(obj, attr)
            if callable(value):
                value = value()
            self.update_data[get_key(obj, attr)] = value

    def form(self, form_obj):
        """ Make form errors available. """
        if not form_obj.is_valid():
            for name, errors in form_obj.errors.items():
                if form_obj.prefix:
                    key = 'id_%s-%s' % (form_obj.prefix, name)
                else:
                    key = 'id_%s' % name
                self.form_data[key] = errors

    def replace(self, element, html):
        """ Replace the given DOM element with the given html. 
            The DOM element is specified using css identifiers.
            Some javascript libraries may have an extended syntax, 
            which can be used if you don't value portability.
        """
        self.replace_data[element] = html

    def hide(self, element):
        """ Hides the given DOM element.
            The DOM element is specified using css identifiers.
            Some javascript libraries may have an extended syntax, 
            which can be used if you don't value portability.
        """
        self.hide_data.append(element)

    def redirect(self, to, *args, **kwargs):
        if hasattr(to, 'get_absolute_url'):
            self.redirect_data = to.get_absolute_url()
            return
        try:
            self.redirect_data = urlresolvers.reverse(to, args=args, kwargs=kwargs)
            return
        except urlresolvers.NoReverseMatch:
            # If this is a callable, re-raise.
            if callable(to):
                raise
            # If this doesn't "feel" like a URL, re-raise.
            if '/' not in to and '.' not in to:
                raise
        
        # Finally, fall back and assume it's a URL
        self.redirect_data = to


    def extra(self, key, value):
        self.extra_data[key] = value

    @property
    def json_response(self):
        """ Return a json response with our ajax data """
        elements = (
            ('extra', self.extra_data),
            ('messages', self.messages_data),
            ('forms', self.form_data),
            ('replace', self.replace_data),
            ('hide', self.hide_data),
            ('update', self.update_data),
            ('redirect', self.redirect_data),
            )
        return JsonResponse(dict((a,b) for a,b in elements if b))

class JsonResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, QuerySet):
            content = serialize('json', obj)
        else:
            content = simplejson.dumps(obj, indent=2, cls=json.DjangoJSONEncoder, ensure_ascii=False)

        super(JsonResponse, self).__init__(content, content_type='application/json')
