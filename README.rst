=============================
Django-Autocode
=============================

.. image:: https://badge.fury.io/py/django-autocode.svg
    :target: https://badge.fury.io/py/django-autocode

.. image:: https://travis-ci.org/lorne-luo/django-autocode.svg?branch=master
    :target: https://travis-ci.org/lorne-luo/django-autocode

.. image:: https://codecov.io/gh/lorne-luo/django-autocode/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/lorne-luo/django-autocode

Automatic code generation

Documentation
-------------

The full documentation is at https://django-autocode.readthedocs.io.

Quickstart
----------

Install django-autocode::

    pip install django-autocode

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    if DEBUG:
        INSTALLED_APPS = +[
            'autocode',
        ]

Add django-autocode's URL patterns:

.. code-block:: python

    if DEBUG:
        urlpatterns += [
            url(r'', include('autocode.urls', namespace='autocode')),
        ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox
