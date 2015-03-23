from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url(r'^reviews/', include('rating.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='profile.html')),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
)
