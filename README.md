# Django-Autocode

Django-Autocode is a [Django](http://www.djangoproject.com/) application that could generate forms/views/urls/api codes for your Django model.


## Installation
```pip install django-autocode```

**settings.py**
```
if DEBUG:
    INSTALLED_APPS = +[
        'autocode',
    ]
```

**urls.py**
```
if DEBUG:
    urlpatterns += [
        url(r'', include('autocode.urls', namespace='autocode')),
    ]
```

## Usage
