# 
# Adjax, a framework for easing the development of Django websites with Ajax.
#

__all__ = ('adjax_response', 'success', 'info', 'warning', 'error', 'debug', 
           'redirect', 'update', 'form', 'replace', 'hide', 'extra',   
           'render_to_response')

__version_info__ = ('1', '0', '0')
__version__ = '.'.join(__version_info__)
__authors__ = ["Will Hardy <adjax@hardysoftware.com.au>"]


from adjax.decorators import adjax_response
from adjax.base import get_store
from django.contrib.messages import success, info, warning, error, debug


def update(request, obj, attributes=None):
    """ Sends the updated version of the given attributes on the given object. 
        If no attributes are given, all attributes are sent (be careful if you
        don't want all data to be public).
        If a minus sign is in front of an attribute, it is omitted.
        A mix of attribtue names with and without minus signs is just silly.
        No other attributes will be included.
    """
    store = get_store(request)
    if not attributes or all(map(lambda s: s.startswith("-"), attributes)):
        attributes = obj.__dict__.keys()
    store.update(obj, (a for a in attributes if not a.startswith("-")))


def form(request, form_obj):
    """ Validate the given form and send errors to browser. """
    get_store(request).form(form_obj)


def replace(request, element, html):
    """ Replace the given DOM element with the given html. 
        The DOM element is specified using css identifiers.
        Some javascript libraries may have an extended syntax, 
        which can be used if you don't value portability.
    """
    get_store(request).replace(element, html)


def redirect(request, path):
    """ Redirect the browser dynamically to another page. """
    get_store(request).redirect(path)


def hide(request, element):
    """ Hides the given DOM element.
        The DOM element is specified using css identifiers.
        Some javascript libraries may have an extended syntax, 
        which can be used if you don't value portability.
    """
    get_store(request).hide(element)


def extra(request, key, value):
    """ Send additional information to the browser. """
    get_store(request).extra(key, value)


def render_to_response(request, template_name, context=None, prefix=None):
    """ Update any included templates. """
    get_store(request).render_to_response(template_name, context, prefix)
