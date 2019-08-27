import inspect
import os
import sys
import types

from django.core.management.base import BaseCommand
from django.db import models
from django.template.loader import get_template
from django.utils.module_loading import import_string

from autocode.autocode import code_groups, template_root, import_model, \
    find_models_by_app_name


class Command(BaseCommand):
    help = ''' Create code

    Usage: ./manage.py code [--overwrite] <module_name>

    Example:

        python manage.py autocode auth

        python manage.py autocode auth.Group

        python manage.py autocode apps/product/

    '''

    args = "app folder path or models.py path"
    module = None
    model_list = []
    is_overwrite = False
    app_name = None
    path = None
    file = []
    files = []

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", "-o", action="store_true", dest="is_overwrite", default=False,
                            help="Overwrite all files.")
        parser.add_argument("--write", "-w", action="store_true", dest="is_write", default=False,
                            help="write all files.")

        parser.add_argument("--view", "-vi", action="store_true", dest="is_view", default=False,
                            help="Generate code for view")

        parser.add_argument("--api", "-a", action="store_true", dest="is_api", default=False,
                            help="Generate code for api")

        parser.add_argument("--template", "-t", action="store_true", dest="is_template", default=False,
                            help="Generate code for template")

        parser.add_argument('path', nargs='?', type=str)
        parser.add_argument('file', nargs='?', type=str, default='all')

    def import_model(self, mod):
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(self.module_str):
                if issubclass(obj, models.Model) and not obj._meta.abstract:
                    self.model_list.append(obj)

    def scan_models(self, module_name):
        self.model_list += find_models_by_app_name(module_name)
        if self.model_list:
            self.app_name = self.model_list[0]._meta.app_label
            return self.model_list

        mod = import_string(module_name)
        if isinstance(mod, types.ModuleType):
            self.module = mod
            self.model_list += import_model(self.module_str, mod)
        elif issubclass(mod, models.Model):
            self.model_list.append(mod)
            self.module = sys.modules[mod.__module__]
        else:
            raise AttributeError('%s is not a model or module' % module_name)

        if not len(self.model_list):
            raise AttributeError('Found no model in %s' % module_name)

        return self.model_list

    def parse_parameters(self, **options):
        self.path = options.get("path")
        self.file = options.get("file")

        if self.file not in code_groups:
            self.stdout.write(f"File arguments should in {list(code_groups.keys())}")
            return

        if options.get("is_view"):
            self.files.append('views')

        if options.get("is_api"):
            self.files.append('api')

        if options.get("is_template"):
            self.files.append('templates')

        self.is_write = options.get("is_write")
        self.is_overwrite = options.get("is_overwrite")

        if not self.files:
            self.files = ['all']

        self.module_str = self.path.replace('.py', '').replace('/', '.').strip('.')
        # self.module_str = self.module_str if '.models' in self.module_str else self.module_str + '.models'

    def handle(self, *args, **options):
        self.parse_parameters(**options)

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

        module_dir = os.path.join(*self.model_list[0].__module__.split('.')[:-1])

        for template_file in self.get_template_files():
            file_name_template = os.path.basename(template_file)[:-1 * len('.html')]
            if '{model}' in file_name_template:
                for model in self.model_list:
                    file_name = file_name_template.format(model=model.__name__.lower())
                    context_data['model'] = model
                    print('=' * 20, file_name.lower(), '=' * 20)
                    template = get_template(template_file)
                    html = self.unescape(template.render(context_data))
                    if self.is_write:
                        path = self.write_file(module_dir, file_name, html)
                        print(f'{file_name} write to {path}')
                    else:
                        print(html)
            else:
                file_name = file_name_template
                print('=' * 20, file_name.lower(), '=' * 20)
                template = get_template(template_file)
                html = self.unescape(template.render(context_data))
                if self.is_write:
                    path = self.write_file(module_dir, file_name, html)
                    print(f'{file_name} write to {path}')
                else:
                    print(html)
        return

    def get_context_data(self):
        context_data = {
            'models': self.model_list,
            'app_name': self.app_name,
            'models_fields': dict([(model.__name__, model._meta.fields)
                                   for model in self.model_list])
        }
        return context_data

    def write_file(self, module_dir, filename, content):
        if filename.endswith('.html'):
            path = os.path.join(module_dir, 'templates', self.app_name, filename)
        elif filename.endswith('.js'):
            path = os.path.join(module_dir, 'static', self.app_name, filename)
        else:
            path = os.path.join(module_dir, filename)

        if os.path.isfile(path) and not self.is_overwrite:
            path += '.code'

        base_dir = os.path.dirname(path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        with open(path, 'w+') as f:
            f.write(content)
        return path

    def get_template_path(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        folder_path = os.path.abspath(os.path.join(file_path, os.pardir, os.pardir, 'templates'))

        return os.path.join(folder_path, 'autocode', 'code', 'api_views.py.html')

    def get_template_files(self):
        templates = []
        for file in self.files:
            if file in code_groups:
                templates += code_groups.get(file, [])

        templates = list(set(templates))
        return [os.path.join(template_root, file_name) for file_name in templates]

    def unescape(self, html):
        return html.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', '\'').replace(
            '&amp;', '&')
