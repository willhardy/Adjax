#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.core.serializers import json, serialize
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet

def get_key(instance, field_name):
    """ Returns the key that will be used to identify dynamic fields in the DOM. """
    # TODO: Avoid any characters that may not appear in class names
    m = instance._meta
    return '-'.join(('data', m.app_label, m.object_name, str(instance.pk), field_name))


class JsonResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, QuerySet):
            content = serialize('json', obj)
        else:
            content = simplejson.dumps(obj, indent=2, cls=json.DjangoJSONEncoder, ensure_ascii=False)

        super(JsonResponse, self).__init__(content, content_type='application/json')
