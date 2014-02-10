from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from .views import Home

urlpatterns = patterns('',
    # Examples:
    url(r'^json/?$', Home.as_view(), name='json'),
    url(r'^$', TemplateView.as_view(template_name="index.html")),

)
