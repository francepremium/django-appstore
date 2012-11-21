from django.conf.urls import patterns, include, url
from django.views import generic

from models import AppFeature, AppCategory
from views import (AppCategoryListView, AppCategoryDetailView, AppDeployView,
        AppDetailView, AppCreateView, AppUpdateView, EnvUpdateView)

urlpatterns = patterns('',
    # Env settings
    url(r'env/(?P<pk>\d+)/$', EnvUpdateView.as_view(),
        name='appstore_env_update'),

    # App editor
    url(r'app/create/$', AppCreateView.as_view(),
        name='appstore_app_create'),
    url(r'app/(?P<pk>\d+)/update/$', AppUpdateView.as_view(),
        name='appstore_app_update'),
    url(r'app/(?P<pk>\d+)/deploy/$', AppDeployView.as_view(),
        name='appstore_app_deploy'),

    # Appstore
    url(r'(?P<pk>\d+)/$', AppDetailView.as_view(),
        name='appstore_app_detail'),
    url(r'(?P<appcategory>\w+)/$', AppCategoryDetailView.as_view(),
        name='appstore_appcategory_detail'),
    url(r'^$', AppCategoryListView.as_view(),
        name='appstore_appcategory_list'),
)
