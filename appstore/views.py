from django.views import generic
from django import http

from models import AppCategory, App


class AppCategoryListView(generic.ListView):
    model = AppCategory


class AppCategoryDetailView(generic.DetailView):
    model = AppCategory

    def get_object(self, queryset=None):
        return self.get_queryset().get(
            name=self.kwargs['appcategory'].replace('--', '/'))


class AppDetailView(generic.DetailView):
    model = App

    def post(self, request, *args, **kwargs):
        environment = request.session['appstore_environment']

        if request.user in environment.users.all():
            if request.POST.get('action', None) == 'install':
                result = environment.install_app(self.get_object())
            elif request.POST.get('action', None) == 'uninstall':
                result = environment.uninstall_app(self.get_object())
            else:
                return http.HttpResponseBadRequest()
            return http.HttpResponse(status=201)
        else:
            return http.HttpResponseForbidden('Not an admin for this env')
