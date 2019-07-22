import inspect
import os
import types
from functools import reduce
from importlib import import_module

from django.apps import apps
from django.db import models
from django.utils.module_loading import import_string

file_path = os.path.dirname(os.path.realpath(__file__))
template_root = os.path.join('autocode', 'code')

code_groups = {
    'all': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html', 'api_views.py.html',
            'serializers.py.html', 'api_views.py.html', 'serializers.py.html'],
    'app': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html'],
    'api': ['serializers.py.html', 'api_views.py.html'],
    'views': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html'],
    'templates': ['{model}_form.html', '{model}_list.html']
}
all_templates = list(set(reduce(list.__add__, code_groups.values())))

py_files = ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html', 'api_views.py.html',
            'serializers.py.html']


def find_model_by_name(model_name):
    all_models = apps.get_models()
    model_list = []
    if model_name[0].isupper():
        for model in all_models:
            if model.__name__ == model_name:
                model_list.append(model)
    return model_list


def find_model_in_module(module):
    result = []
    for name, obj in inspect.getmembers(module, inspect.ismodule):
        if name in ['models', 'model']:
            result += find_model_in_module(obj)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj is not models.Model and issubclass(obj, models.Model):
            if not obj._meta.abstract:
                result.append(obj)
    return result


def import_model(module_str, mod):
    result = []
    for name, obj in inspect.getmembers(mod, inspect.isclass):
        if obj.__module__.startswith(module_str):
            if issubclass(obj, models.Model) and not obj._meta.abstract:
                result.append(obj)
    return result


def find_models_by_app_name(app_name):
    all_models = apps.get_models()
    model_list = []
    for model in all_models:
        if model._meta.app_label == app_name:
            model_list.append(model)
    if model_list:
        return model_list

    for model in all_models:
        if model.__name__ == app_name:
            model_list.append(model)
    if model_list:
        return model_list

    for model in all_models:
        if model._meta.label == app_name:
            model_list.append(model)
    if model_list:
        return model_list

    model_name=''
    if app_name.split('.')[-1][0].isupper():
        model_name=app_name.split('.')[-1]
        app_name=app_name.replace('.%s'% model_name,'')
    print(app_name,model_name)
    for model in all_models:
        if model.__module__.startswith( app_name):
            if model_name:
                if model_name ==model.__name__:
                    model_list.append(model)
            else:
                model_list.append(model)
    if model_list:
        return model_list

    return []


def find_models_by_app_path(app_name):
    module_str = f'{app_name}.models' if not app_name.endswith('.models') else app_name
    module = import_module(module_str)

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
