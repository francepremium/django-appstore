from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

import rules_light
rules_light.autodiscover()

import autocomplete_light
autocomplete_light.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_project.views.home', name='home'),
    # url(r'^test_project/', include('test_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^appstore/', include('appstore.urls')),
    url(r'^form_designer/', include('form_designer.urls')),
    url(r'^dummy_appeditor/',
        include('appstore.contrib.dummy_appeditor.urls')),
    url(r'^form_designer_appeditor/',
        include('appstore.contrib.form_designer_appeditor.urls')),
    url(r'^autocomplete_light/', include('autocomplete_light.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

