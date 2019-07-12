=====
Usage
=====

To use django-autocode in a project, add it to your `INSTALLED_APPS`:

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
