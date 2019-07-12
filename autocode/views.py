from django.http import Http404
from django.views.generic import TemplateView

from autocode.autocode import find_models_by_app_name


class AppCodeView(TemplateView):
    template_name = 'autocode/base.html'

    def get(self, request, *args, **kwargs):
        app_name = kwargs.get('app_name', None)
        if not app_name:
            raise Http404

        model_list = find_models_by_app_name(app_name)
        print(model_list)
        return super(AppCodeView, self).get(request, *args, **kwargs)
