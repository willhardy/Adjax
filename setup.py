# -*- coding: UTF-8 -*-

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "Adjax",
    version = "1.0",
    packages = find_packages(exclude=["website*", "tests*", "design*"]),
    install_requires = ['django>=1.0'],
    author = "Will Hardy",
    author_email = "adjax@hardysoftware.com.au",
    description = "",
    license = "New BSD",
    keywords = "",
    url = "http://adjax.hardysoftware.com.au/",
    package_data = {
        'adjax': ['media/js/*.js'],
        }

)

