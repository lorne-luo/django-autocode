import inspect
import os
from functools import reduce
from importlib import import_module

from django.db import models

file_path = os.path.dirname(os.path.realpath(__file__))
template_root = os.path.abspath(os.path.join(file_path, 'templates', 'autocode', 'code'))

code_groups = {
    'all': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html', 'api_views.py.html',
            'serializers.py.html', 'api_views.py.html', 'serializers.py.html'],
    'app': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html'],
    'views': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html'],
    'templates': ['{model_name}_form.html', '{model_name}_list.html']
}
all_templates = list(set(reduce(list.__add__, code_groups.values())))

py_files = ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html', 'api_views.py.html',
            'serializers.py.html']


def find_models_by_app_name(app_name):
    module = import_module(f'{app_name}.models')

    model_list = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, models.Model) and not obj._meta.abstract:
            model_list.append(obj)
    return model_list


def get_fields_and_labels(model):
    titles = []
    fields = []

    # normal fields + many-to-many fields
    meta_fields = model._meta.fields + model._meta.many_to_many
    for mf in meta_fields:
        if mf.name in ['id', 'pk']:
            continue
        elif isinstance(mf, models.fields.DateTimeField):
            if mf.auto_now_add or mf.auto_now:
                continue
        fields.append(mf.name)
        title = str(mf.verbose_name)
        if title and title[0].islower():
            title = title.title()
        titles.append(title)
    return fields, titles
