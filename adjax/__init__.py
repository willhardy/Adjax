# 
# Adjax, a framework for easing the development of Django websites with Ajax.
#

from adjax.api import redirect, update, form, replace, hide, extra
from adjax.api import render, render_to_response, response
from adjax.decorators import adjax_response
from django.contrib.messages import success, info, warning, error, debug

# Version information

VERSION = (1, 1, 0, 'alpha', 0)
__version_info__ = tuple(str(v) for v in VERSION[:3])
__version__ = '.'.join(__version_info__)
__authors__ = ["Will Hardy <adjax@hardysoftware.com.au>"]

def get_version():
    version = '.'.join(VERSION[:2])
    # Maintenance releases
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    # Pre-release versions
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    elif VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version
