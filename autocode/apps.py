from django.apps import AppConfig
from django.contrib import admin


class AutomodelAppConfig(AppConfig):
    name = 'rosetta'

    def ready(self):
        admin.site.index_template = 'rosetta/admin_index.html'
