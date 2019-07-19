import sys

import inspect
import os
import types
from pprint import pprint

from django.core import management
from django.core.management.base import BaseCommand
from django.db import models
from django.template.loader import get_template
from django.utils.module_loading import import_string

from .templates.api_serializers import SERIALIZERS_HEADER, SERIALIZERS_BODY
from .templates.api_urls import API_URLS_HEADER, API_URLS_BODY, API_URLS_FOOTER
from .templates.api_views import API_VIEWS_HEADER, API_VIEWS_BODY
from .templates.forms import FORMS_HEADER, FORMS_BODY
from .templates.templates import LIST_JS, LIST_TEMPLATES, MENU_TEMPLATE, MENU_APP_TEMPLATE, TABLE_HEAD_TEMPLATES, \
    TABLE_ROW_TEMPLATES
from .templates.urls import URLS_HEADER, URLS_BODY, URLS_FOOTER
from .templates.views import VIEWS_HEADER, VIEWS_BODY


class Command(BaseCommand):
    help = ''' Create code

    Usage: ./manage.py code [--overwrite] <module_name>

    Example:

        ./manage.py code apps.product

        ./manage.py code -o apps.product.models.Product

        ./manage.py code apps/product/

    '''

    args = "app folder path or models.py path"
    module = None
    model_list = []
    is_overwrite = False

    # template = get_template(template_src)
    # html = template.render(context_dict)

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", "-o", action="store_true", dest="is_overwrite", default=False,
                            help="Overwrite all files.")
        parser.add_argument('path', nargs='+', type=str)


    def import_model(self, mod):
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(self.module_str):
                if issubclass(obj, models.Model) and not obj._meta.abstract:
                    self.model_list.append(obj)

    def scan_models(self, name):
        mod = import_string(name)
        if isinstance(mod, types.ModuleType):
            self.module = mod
            self.import_model(mod)
        elif issubclass(mod, models.Model):
            self.model_list.append(mod)
            self.module = sys.modules[mod.__module__]
        else:
            raise AttributeError('%s is not a model or module' % name)

        if not len(self.model_list):
            raise AttributeError('Found no model in %s' % name)

        self.app_name = self.model_list[0]._meta.app_label
        self.app_str = self.module_str[:self.module_str.find('.models')]
        self.module_file = self.module.__file__[:-1]
        self.module_folder = os.path.dirname(self.module.__file__)
        self.serializers_file = os.path.join(self.module_folder, 'api', 'serializers.py')
        self.api_urls_file = os.path.join(self.module_folder, 'api', 'urls.py')
        self.api_views_file = os.path.join(self.module_folder, 'api', 'views.py')
        self.views_file = os.path.join(self.module_folder, 'views.py')
        self.urls_file = os.path.join(self.module_folder, 'urls.py')
        self.forms_file = os.path.join(self.module_folder, 'forms.py')
        self.js_folder = os.path.join(self.module_folder, 'static', 'js', self.app_name, '%s_list.js')
        self.templates_folder = os.path.join(self.module_folder, 'templates', self.app_name, '%s_list.html')
        self.menu_html_file = os.path.join(self.module_folder, 'templates', self.app_name, '_menu.html')
        self.all_models_str = ', '.join([md.__name__ for md in self.model_list])

    def handle(self, *args, **options):
        params = options.get("path")
        if len(params) < 1:
            self.stderr.write(self.help)
            return
        self.is_overwrite = options.get("is_overwrite")

        path = params[0]
        self.module_str = path.replace('.py', '').replace('/', '.').strip('.')
        self.module_str = self.module_str if '.models' in self.module_str else self.module_str + '.models'

        try:
            self.scan_models(self.module_str)
        except AttributeError as e:
            self.stdout.write("Error: %s" % e)
            return
        context_data={}
        context_data['models'] = self.model_list
        context_data['app_name'] = 'example'
        context_data['models_fields'] = dict([(model.__name__, model._meta.fields)
                                         for model in self.model_list])
        pprint(context_data)
        print(self.get_template_path())

        template = get_template(self.get_template_path())
        html = template.render(context_data)
        print(html)
        return

    def get_template_path(self):
        file_path=os.path.dirname(os.path.realpath(__file__))
        folder_path=os.path.abspath(os.path.join(file_path, os.pardir, os.pardir,'templates'))

        return os.path.join(folder_path,'autocode','code','api_views.html')
