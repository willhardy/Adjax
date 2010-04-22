# -*- coding: UTF-8 -*-

from django import template
from django.template.loader import get_template
from adjax.utils import get_key, get_template_include_key
from django.conf import settings


register = template.Library()


def adjax(parser, token):
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
        if hasattr(instance, '_meta'):
            return '<span class="%s">%s</span>' % (get_key(instance, self.field_name), self.value.resolve(context))


def adjax_include(parser, token):
    bits = token.split_contents()
    try:
        tag_name, template_name = bits[:2]
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a template name" % bits[0]

    kwargs = {}
    for arg in bits[2:]:
        key, value = arg.split("=", 1)
        if key in ('prefix', 'wrapper'):
            kwargs[str(key)] = value
        else:
            raise template.TemplateSyntaxError, "invalid argument (%s) for %r tag" % (key, tag_name)

    return AdjaxIncludeNode(template_name, **kwargs)


class AdjaxIncludeNode(template.Node):

    def __init__(self, template_name, prefix=None, wrapper='"div"'):
        self.template_name = template.Variable(template_name)
        self.prefix = prefix and template.Variable(prefix) or None
        self.wrapper = template.Variable(wrapper)


    def render(self, context):
        template_name = self.template_name.resolve(context)
        wrapper = self.wrapper.resolve(context)
        prefix = self.prefix and self.prefix.resolve(context) or None
        key = get_template_include_key(template_name, prefix)
        try:
            content = get_template(template_name).render(context)
            return '<%s class="%s">%s</%s>' % (wrapper, key, content, wrapper)
        except template.TemplateSyntaxError, e:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''
        except:
            return '' # Like Django, fail silently for invalid included templates.


# Register our tags
register.tag('adjax', adjax)
register.tag('adjax_include', adjax_include)

