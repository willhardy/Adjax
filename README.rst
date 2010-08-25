=====
Adjax
=====

Adjax is a small framework to streamline the building of ajax-based sites using
the Django web development framework. 

Please visit http://adjax.hardysoftware.com.au/ for an introduction.


Documentation
=============

Comprehensive documentation for Adjax can be found in the ``docs/`` directory or
online at http://readthedocs.org/willhardy/adjax/. The documentation includes:

- full installation details
- tutorial
- reference guide
- best Ajax practices overview, and
- a developers guide (for those who would like to contribute).


Quick Installation
==================

If you have pip installed:

    pip install adjax

Or download the release, unpack and run:

    python ./setup.py install

If you are interested in the development version, you can download it here:

    git clone git@github.com:willhardy/Adjax.git


Demonstration
=============

A quick demonstration of Adjax in operation can be found in the tests.
Move into the ``tests/`` folder and run the test server:

    cd tests
    python ./manage.py syncdb --noinput
    python ./manage.py runserver

Now open a browser up to http://localhost:8000/demo/


Contributors
============

People who have contributed to Adjax are:

- Will Hardy
- Goran Stefkovski

