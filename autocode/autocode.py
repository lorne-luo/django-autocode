import inspect
import os
from collections import defaultdict
from functools import reduce
from importlib import import_module

from django.apps import apps
from django.db import models
from django.template import engines

file_path = os.path.dirname(os.path.realpath(__file__))
template_root = os.path.join('autocode', 'code')

code_groups = {
    'app': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html'],
    'api': ['api__serializers.py.html', 'api__views.py.html'],
    'views': ['views.py.html', 'admin.py.html', 'forms.py.html', 'urls.py.html'],
    'templates': ['templates__{module}__{model}_form.html.html', 'templates__{module}__{model}_list.html.html'],
    'graphql': ['graphql__schema.py.html', 'graphql__query.py.html', 'graphql__mutation.py.html'],
    'tests': ['tests__test_query.py.html', 'tests__test_mutation.py.html']
}
code_groups['__all__'] = list(set(reduce(list.__add__, code_groups.values())))


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

    model_name = ''
    if app_name.split('.')[-1][0].isupper():
        model_name = app_name.split('.')[-1]
        app_name = app_name.replace('.%s' % model_name, '')
    print(app_name, model_name)
    for model in all_models:
        if model._meta.abstract:
            continue

        if model.__module__.startswith(app_name):
            if model_name:
                if model_name == model.__name__:
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


def get_template_dirs(app_name):
    engines_list = engines.all()
    template_roots = reduce(list.__add__, [en.dirs for en in engines_list])

    app_template_list = reduce(list.__add__, [en.template_dirs for en in engines_list])
    get_app = lambda x: x.rsplit(os.path.sep, 2)[-2]
    app_templates = dict([(get_app(temp), temp) for temp in app_template_list if temp not in template_roots])

    file_path = os.path.dirname(os.path.realpath(__file__))
    default_template = os.path.abspath(os.path.join(file_path, 'templates'))
    template_roots += [default_template]

    if app_templates.get(app_name):
        template_roots = [app_templates.get(app_name)] + template_roots

    return tuple(template_roots)


def list_template_file(app_name):
    template_dirs = get_template_dirs(app_name)
    sub_path = os.path.join('autocode', 'code')
    templates = {}
    for temp in template_dirs:
        path = os.path.join(temp, sub_path)
        for file in os.listdir(path):
            if file.endswith(".html"):
                if file not in templates:
                    templates[file] = os.path.join(path, file)

    return templates


def get_code_groups(app_name):
    splitter = '__'
    templates = list_template_file(app_name)
    result = defaultdict(lambda: [])

    for file_name, path in templates.items():
        folder = file_name.split(splitter)[0] if splitter in file_name else '__root__'
        result[folder] += [path]
        result['__all__'] += [path]

    return result
