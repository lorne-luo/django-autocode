import inspect
import os
import sys
import types

from django.core.management.base import BaseCommand
from django.db import models
from django.template.loader import get_template
from django.utils.module_loading import import_string

from autocode.autocode import find_models_by_app_name, code_groups, template_root


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
    app_name = None
    path = None
    file = None

    # template = get_template(template_src)
    # html = template.render(context_dict)

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", "-o", action="store_true", dest="is_overwrite", default=False,
                            help="Overwrite all files.")
        parser.add_argument('path', nargs='?', type=str)
        parser.add_argument('file', nargs='?', type=str, default='all')

    def import_model(self, mod):
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(self.module_str):
                if issubclass(obj, models.Model) and not obj._meta.abstract:
                    self.model_list.append(obj)

    def scan_models(self, module_name):
        if '.' not in module_name and '/' not in module_name:
            self.model_list = find_models_by_app_name(module_name)
            self.app_name = module_name
            return

        mod = import_string(module_name)
        if isinstance(mod, types.ModuleType):
            self.module = mod
            self.import_model(mod)
        elif issubclass(mod, models.Model):
            self.model_list.append(mod)
            self.module = sys.modules[mod.__module__]
        else:
            raise AttributeError('%s is not a model or module' % module_name)

        if not len(self.model_list):
            raise AttributeError('Found no model in %s' % module_name)

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
        self.path = options.get("path")
        self.file = options.get("file")

        if self.file not in code_groups:
            self.stdout.write(f"File arguments should in {list(code_groups.keys())}")
            return

        self.is_overwrite = options.get("is_overwrite")

        self.module_str = self.path.replace('.py', '').replace('/', '.').strip('.')
        self.module_str = self.module_str if '.models' in self.module_str else self.module_str + '.models'

        try:
            self.scan_models(self.module_str)
        except AttributeError as e:
            self.stdout.write("Error: %s" % e)
            return
        except Exception as e:
            self.stdout.write('No models found.')
            return

        if not self.model_list:
            self.stdout.write('No models found.')
            return
        else:
            self.app_name = self.model_list[0]._meta.app_label

        context_data = self.get_context_data()

        for template_file in self.get_template_files():
            file_name = os.path.basename(template_file)
            if '{model}' in file_name:
                file_name = os.path.basename(template_file)
                for model in self.model_list:
                    file_name = file_name.format(model=model.__name__)
                    context_data['model'] = model

                    print('=' * 20, file_name, '=' * 20)
                    template = get_template(template_file)
                    html = template.render(context_data)
                    print(self.unescape(html))
            else:
                file_name = file_name.strip('.html')
                print('=' * 20, file_name, '=' * 20)
                template = get_template(template_file)
                html = template.render(context_data)
                print(self.unescape(html))
            # todo template need loop models
        return

    def get_context_data(self):
        context_data = {
            'models': self.model_list,
            'app_name': self.app_name,
            'models_fields': dict([(model.__name__, model._meta.fields)
                                   for model in self.model_list])
        }
        return context_data

    def get_template_path(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        folder_path = os.path.abspath(os.path.join(file_path, os.pardir, os.pardir, 'templates'))

        return os.path.join(folder_path, 'autocode', 'code', 'api_views.py.html')

    def get_template_files(self):
        return [os.path.join(template_root, file_name) for file_name in code_groups[self.file]]

    def unescape(self, html):
        return html.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', '\'').replace(
            '&amp;', '&')
