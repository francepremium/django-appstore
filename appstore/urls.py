from django.conf.urls import patterns, include, url
from django.views import generic

from models import AppFeature, AppCategory
from views import (AppCategoryListView, AppCategoryDetailView, AppDeployView,
    AppDetailView, AppCreateView, AppUpdateView, EnvUpdateView, EnvCreateView,
    UserEnvironmentListView, UserEnvironmentUpdateView, EnvActivateView,
    UserEnvironmentDeleteView, UserEnvironmentCreateView)

urlpatterns = patterns('',
    url(r'env/create/$', EnvCreateView.as_view(),
        name='appstore_env_create'),
    url(r'env/activate/(?P<pk>\d+)/$', EnvActivateView.as_view(),
        name='appstore_env_activate'),
    url(r'env/(?P<pk>\d+)/update/$', EnvUpdateView.as_view(),
        name='appstore_env_update'),

    url(r'env/(?P<env_pk>\d+)/users/$', UserEnvironmentListView.as_view(),
        name='appstore_userenvironment_list'),
    url(r'env/(?P<env_pk>\d+)/users/create/$',
        UserEnvironmentCreateView.as_view(),
        name='appstore_userenvironment_create'),
    url(r'env/(?P<pk>\d+)/users/update/$', UserEnvironmentUpdateView.as_view(),
        name='appstore_userenvironment_update'),
    url(r'env/(?P<pk>\d+)/users/delete/$', UserEnvironmentDeleteView.as_view(),
        name='appstore_userenvironment_delete'),

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
