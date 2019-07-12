=============================
django-autocode
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

    INSTALLED_APPS = (
        ...
        'autocode.apps.AutocodeConfig',
        ...
    )

Add django-autocode's URL patterns:

.. code-block:: python

    from autocode import urls as autocode_urls


    urlpatterns = [
        ...
        url(r'^', include(autocode_urls)),
        ...
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

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
