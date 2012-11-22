from django.conf.urls import patterns, include, url
from django.views import generic

from views import DummyAppUpdateView


urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/update/$', DummyAppUpdateView.as_view(),
        name='dummy_appeditor_dummyapp_update'),
)
