from django import template
from django.utils.text import re_camel_case

register = template.Library()


@register.filter(name='get')
def get(d, k):
    return d.get(k, None)


@register.filter(name='get_name')
def get_name(model):
    return model._meta.object_name


@register.filter(name='get_var')
def get_var(model):
    """python var name: CompanyInfo -> company_info"""
    name = model._meta.object_name
    return re_camel_case.sub(r'_\1', name).strip('_').lower()


@register.filter(name='get_app')
def get_app(model):
    return model._meta.app_label


@register.filter(name='get_model_label')
def get_model_label(model):
    return model._meta.label


@register.filter(name='list_models')
def list_models(models, suffix=''):
    return ', '.join([m._meta.object_name + suffix for m in models])


@register.filter(name='list_field_names')
def list_field_names(model, ignore_pk=False):
    if ignore_pk:
        return '["%s"]' % '", "'.join([f.name for f in model._meta.fields if f.name not in ['pk', 'id']])
    return '["%s"]' % '", "'.join([f.name for f in model._meta.fields])


@register.filter(name='list_fields')
def list_fields(model, ignore_pk=False):
    if ignore_pk:
        return [x for x in model._meta.fields if x.name not in ['id', 'pk']]

    return model._meta.fields
