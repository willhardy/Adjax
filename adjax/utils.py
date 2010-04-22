# -*- coding: UTF-8 -*-

from django.core.serializers import json, serialize
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet

try:
    import hashlib
    hash_function = hashlib.sha1
except ImportError:
    import sha
    hash_function = sha.new


def get_key(instance, field_name):
    """ Returns the key that will be used to identify dynamic fields in the DOM. """
    # TODO: Avoid any characters that may not appear in class names
    m = instance._meta
    return '-'.join(('data', m.app_label, m.object_name, str(instance.pk), field_name))


def get_template_include_key(template_name, prefix=None):
    """ Get a valid element class name, we'll stick to ascii letters, numbers and hyphens.
        NB class names cannot start with a hyphen
    """
    digest = int(hash_function(template_name).hexdigest(),16)
    hash = base36.from_decimal(digest)
    if prefix:
        return 'tpl-%s-%s' % (prefix, hash)
    else:
        return 'tpl-%s' % (hash)


class JsonResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, QuerySet):
            content = serialize('json', obj)
        else:
            content = simplejson.dumps(obj, indent=2, cls=json.DjangoJSONEncoder, ensure_ascii=False)

        super(JsonResponse, self).__init__(content, content_type='application/json')


"""
Convert numbers from base 10 integers to base X strings and back again.

Sample usage:

>>> base20 = BaseConverter('0123456789abcdefghij')
>>> base20.from_decimal(1234)
'31e'
>>> base20.to_decimal('31e')
1234

From http://www.djangosnippets.org/snippets/1431/

"""

class BaseConverter(object):
    decimal_digits = "0123456789"
    
    def __init__(self, digits):
        self.digits = digits
    
    def from_decimal(self, i):
        return self.convert(i, self.decimal_digits, self.digits)
    
    def to_decimal(self, s):
        return int(self.convert(s, self.digits, self.decimal_digits))
    
    def convert(number, fromdigits, todigits):
        # Based on http://code.activestate.com/recipes/111286/
        if str(number)[0] == '-':
            number = str(number)[1:]
            neg = 1
        else:
            neg = 0

        # make an integer out of the number
        x = 0
        for digit in str(number):
           x = x * len(fromdigits) + fromdigits.index(digit)
    
        # create the result in base 'len(todigits)'
        if x == 0:
            res = todigits[0]
        else:
            res = ""
            while x > 0:
                digit = x % len(todigits)
                res = todigits[digit] + res
                x = int(x / len(todigits))
            if neg:
                res = '-' + res
        return res
    convert = staticmethod(convert)

base36 = BaseConverter('0123456789abcdefghijklmnopqrstuvwxyz')
