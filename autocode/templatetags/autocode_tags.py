from django import template

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
def list_models(models):
    return ', '.join([m._meta.object_name for m in models])


@register.filter(name='list_fields')
def list_fields(model):
    return '["%s"]' % '", "'.join([f.name for f in model._meta.fields])
