from django.apps import AppConfig
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class myAppNameConfig(AppConfig):
    name = 'example'
    verbose_name = 'An example app'
