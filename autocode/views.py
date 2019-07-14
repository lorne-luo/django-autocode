from django.http import Http404
from django.views.generic import TemplateView

from autocode.autocode import find_models_by_app_name


class BaseCodeView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(BaseCodeView, self).get_context_data(**kwargs)
        app_name = kwargs.get('app_name', None)
        model_name = kwargs.get('model_name', None)
        if not app_name:
            raise Http404

        model_list = find_models_by_app_name(app_name)

        if model_name:
            model_list = list(filter(lambda x: x.__name__.lower() == model_name.lower(), model_list))
            if not model_list:
                raise Http404

        context['models'] = model_list
        context['models_fields'] = dict([(model.__name__, model._meta.fields)
                                         for model in model_list])
        return context


class ModelCodeView(BaseCodeView):
    template_name = 'autocode/model.html'


class AppCodeView(BaseCodeView):
    template_name = 'autocode/app.html'
