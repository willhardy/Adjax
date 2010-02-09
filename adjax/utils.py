#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def AjaxResponse(instance, field_names, context=None):
    """ Helps return a value that can be processed for dynamic fields. """
    if not context:
        context = {}

    if isinstance(field_names, basestring):
        field_names = [field_names]

    data = context.get('data', {})
    data.update(dict([(get_key(instance, f), getattr(instance, f)) for f in field_names ]))
    return {'data': data}

def get_key(instance, field_name):
    """ Returns the key that will be used to identify dynamic fields in the DOM. """
    # TODO: Avoid any characters that may not appear in class names
    m = instance._meta
    return '.' + '-'.join(('data', m.app_label, m.object_name, str(instance.pk), field_name))


