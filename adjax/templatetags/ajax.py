#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import template
from adjax.utils import get_key

register = template.Library()

def ajax(parser, token):
    try:
        tag_name, object_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return DynamicValueNode(object_name)

class DynamicValueNode(template.Node):
    def __init__(self, object_name):
        self.object_name, self.field_name = object_name.rsplit(".", 1)
        self.instance = template.Variable(self.object_name)
        self.value = template.Variable(object_name)
    def render(self, context):
        instance = self.instance.resolve(context)
        if hasattr(instance, '_meta') and instance.pk:
            return '<span class="%s">%s</span>' % (get_key(instance, self.field_name), self.value.resolve(context))

register.tag('ajax', ajax)

