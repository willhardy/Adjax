#!/usr/bin/env python
# -*- coding: UTF-8 -*-

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages
setup(
    name = "Adjax",
    version = "1.0.1",
    packages = find_packages(exclude=["website*", "tests*", "design*"]),
    install_requires = ['django>=1.0'],
    author = "Will Hardy",
    author_email = "adjax@hardysoftware.com.au",
    description = "A framework for easing the development of Django sites with Ajax.",
    license = "New BSD",
    keywords = "ajax, django, framework",
    url = "http://adjax.hardysoftware.com.au/",
    package_data = {
        'adjax': ['media/js/*.js'],
        }

)

