from django.conf.urls import patterns, include, url

from views import AppFormUpdateView

urlpatterns = patterns('',
    url(r'(?P<app_pk>\d+)/$', AppFormUpdateView.as_view(),
        name='form_designer_appeditor_appform_update'),
)
