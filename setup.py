#!/usr/bin/env python
# -*- coding: UTF-8 -*-

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages

version = __import__('adjax').get_version().replace(" ", "-")

setup(
    name = "Adjax",
    version = version,
    packages = find_packages(exclude=["website*", "tests*"]),
    install_requires = ['django>=1.0'],
    author = "Will Hardy",
    author_email = "adjax@hardysoftware.com.au",
    description = "A framework for easing the development of Django sites with Ajax.",
    long_description = open('README.rst').read(),
    license = "LICENSE.txt",
    keywords = "ajax, django, framework",
    url = "http://adjax.hardysoftware.com.au/",
    include_package_data = True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)

