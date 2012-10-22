from django.views import generic
from django import http

from taggit.models import Tag

from models import AppCategory, App
from exceptions import (AppAlreadyInstalled, AppVersionNotInstalled,
        CannotUninstallDependency)


class AppCategoryListView(generic.ListView):
    model = AppCategory


class AppCategoryDetailView(generic.DetailView):
    model = AppCategory

    def get_object(self, queryset=None):
        return self.get_queryset().get(
            name=self.kwargs['appcategory'].replace('--', '/'))

    def get_context_data(self, **kwargs):
        context = super(AppCategoryDetailView, self).get_context_data(
            **kwargs)

        context['appcategory_list'] = AppCategory.objects.all()
        context['app_list'] = context['object'].app_set.filter(
            in_appstore=True)
        context['tag_list'] = Tag.objects.filter(
            app__in=context['app_list']).distinct()

        if self.request.GET.get('tag', None):
            context['app_list'] = context['app_list'].filter(
                tags__name=self.request.GET['tag'])

        return context


class AppDetailView(generic.DetailView):
    model = App

    def post(self, request, *args, **kwargs):
        environment = request.session['appstore_environment']
        app = self.get_object()

        if request.user in environment.users.all():
            try:
                if request.POST.get('action', None) == 'install':
                    result = environment.install_app(app)
                elif request.POST.get('action', None) == 'uninstall':
                    result = environment.uninstall_app(app)
                elif request.POST.get('action', None) == 'fork':
                    fork = app.fork(request.user)
                    result = environment.install_app(fork)
                    environment.uninstall_app(app)
                else:
                    return http.HttpResponseBadRequest('Unknon action')
            except AppAlreadyInstalled:
                return http.HttpResponseBadRequest('App already installed')
            except CannotUninstallDependency:
                return http.HttpResponseBadRequest(
                    'Cannot uninstall dependency')

            return http.HttpResponse(status=201)
        else:
            return http.HttpResponseForbidden('Not an admin for this env')
