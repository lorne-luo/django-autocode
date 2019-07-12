import inspect
from importlib import import_module

from django.db import models


def find_models_by_app_name(app_name):
    module = import_module(f'{app_name}.models')

    model_list = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, models.Model) and not obj._meta.abstract:
            model_list.append(obj)
    return model_list
