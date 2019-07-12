from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'autocode'
urlpatterns = [
    # url(r'', TemplateView.as_view(template_name="base.html")),

    url(r'^autocode/(?P<app_name>[\w\-_\.]+)/$', views.AppCodeView.as_view(), name=f'{app_name}-all'),
]
