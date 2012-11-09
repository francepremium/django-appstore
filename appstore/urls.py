from django.conf.urls import patterns, include, url

from views import (AppCategoryListView, AppCategoryDetailView,
        AppDetailView, EnvUpdateView)

urlpatterns = patterns('',
    url(r'env/(?P<pk>\d+)/$', EnvUpdateView.as_view(),
        name='appstore_env_update'),
    url(r'(?P<pk>\d+)/$', AppDetailView.as_view(),
        name='appstore_app_detail'),
    url(r'(?P<appcategory>\w+)/$', AppCategoryDetailView.as_view(),
        name='appstore_appcategory_detail'),
    url(r'^$', AppCategoryListView.as_view(),
        name='appstore_appcategory_list'),
)
