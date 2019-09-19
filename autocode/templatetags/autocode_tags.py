import stringcase
from django import template
from django.utils.text import re_camel_case

register = template.Library()


@register.filter(name='get')
def get(d, k):
    return d.get(k, None)


@register.filter(name='get_name')
def get_name(model):
    return model._meta.object_name


@register.filter(name='get_app')
def get_app(model):
    return model._meta.app_label


@register.filter(name='get_model_label')
def get_model_label(model):
    return model._meta.label


@register.filter(name='list_models')
def list_models(models, suffix=''):
    return ', '.join([m._meta.object_name + suffix for m in models])


@register.filter(name='list_field_names_exclude')
def list_field_names_exclude(model, args=''):
    arg_list = [arg.strip() for arg in args.split(',')]
    return '["%s"]' % '", "'.join(
        [f.name for f in model._meta.fields if f.name not in arg_list and not f.name.endswith('_ptr')])


@register.filter(name='list_field_names')
def list_field_names(model):
    return '["%s"]' % '", "'.join([f.name for f in model._meta.fields if not f.name.endswith('_ptr')])


@register.filter(name='list_field_names_no_pk')
def list_field_names_no_pk(model):
    return '["%s"]' % '", "'.join(
        [f.name for f in model._meta.fields if f.name not in ['pk', 'id'] and not f.name.endswith('_ptr')])


@register.filter(name='get_fields')
def get_fields(model):
    return [x for x in model._meta.fields if not x.name.endswith('_ptr')]


@register.filter(name='get_fields_exclude')
def get_fields_exclude(model, args=''):
    arg_list = [arg.strip() for arg in args.split(',')]
    return [x for x in model._meta.fields if x.name not in arg_list and not x.name.endswith('_ptr')]


@register.filter(name='get_fields_no_pk')
def get_fields_no_pk(model):
    return get_fields_exclude(model, 'id,pk')


@register.filter(name='get_fields_in')
def get_fields_in(model, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return [x for x in model._meta.fields if x.name in arg_list]


@register.filter(name='get_field_name')
def get_field_name(field):
    if field.__class__.__name__ in ['OneToOneField', 'ForeignKey']:
        return f'{field.name}_id'
    return field.name


@register.filter(name='get_field_type')
def get_field_type(field):
    if not field:
        return None
    return field.__class__.__name__


@register.filter(name='is_required')
def is_required(field):
    if field.null == field.blank == False:
        return True
    return False


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
        'ForeignKey': 'ID',
        'OneToOneField': 'ID',
    }

    return django_graphql_type_maps.get(type_name, 'NameError')


@register.filter(name='snakecase')
def snakecase(string):
    return stringcase.snakecase(str(string))


@register.filter(name='camelcase')
def camelcase(string):
    return stringcase.camelcase(str(string))
