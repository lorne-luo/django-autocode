from django import template
from django.utils.text import re_camel_case
import stringcase

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


@register.filter(name='list_field_names_no_pk')
def list_field_names_no_pk(model, ignore_pk=False):
    return '["%s"]' % '", "'.join([f.name for f in model._meta.fields if f.name not in ['pk', 'id']])


@register.filter(name='get_fields')
def get_fields(model, ignore_pk=False):
    if ignore_pk:
        return [x for x in model._meta.fields if x.name not in ['id', 'pk'] and not x.name.endswith('Ptr')]

    return [x for x in model._meta.fields if not x.name.endswith('Ptr')]


@register.filter(name='get_fields_no_pk')
def get_fields_no_pk(model):
    return [x for x in model._meta.fields if x.name not in ['id', 'pk'] and not x.name.endswith('Ptr')]


@register.filter(name='get_graphql_type')
def get_graphql_type(field):
    type_name = field.__class__.__name__
    django_graphql_type_maps = {
        'AutoField': 'ID',
        'CharField': 'String',
        'TextField': 'String',
        'DateField': 'String',
        'DateTimeField': 'String',
        'TimeField': 'String',
        'EmailField': 'String',
        'FileField': 'String',
        'ImageField': 'String',
        'URLField': 'String',
        'UUIDField': 'String',
        'IntegerField': 'Int',
        'SmallIntegerField': 'Int',
        'BigegerField': 'Int',
        'FloatField': 'Float',
        'DecimalField': 'Float',
        'BooleanField': 'Boolean',
        'NullBooleanField': 'Boolean',
    }

    return django_graphql_type_maps.get(type_name, 'NameError')


@register.filter(name='snakecase')
def snakecase(string):
    return stringcase.snakecase(str(string))


@register.filter(name='camelcase')
def camelcase(string):
    return stringcase.camelcase(str(string))
