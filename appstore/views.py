from django.contrib.sites.models import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views import generic
from django import http
from django.conf import settings
from django.contrib import messages

import rules_light
from taggit.models import Tag

from forms import EnvironmentForm, AppForm, UserEnvironmentCreateForm
from models import Environment, AppCategory, App, UserEnvironment
from exceptions import AppstoreException, CannotEditDeployedApp


@rules_light.class_decorator
class EnvCreateView(generic.CreateView):
    model = Environment
    form_class = EnvironmentForm

    def form_valid(self, form):
        env = form.save()
        UserEnvironment.objects.create(user=self.request.user, environment=env,
                                       is_admin=True)
        self.request.session['appstore_environment'] = env
        return http.HttpResponseRedirect('/')


class EnvActivateView(generic.DetailView):
    model = Environment

    def get(self, request, *args, **kwargs):
        env = self.get_object()

        rules_light.require(request.user, 'appstore.environment.read', env)

        request.session['appstore_environment'] = env
        return http.HttpResponseRedirect('/')


class UserEnvironmentListView(generic.ListView):
    model = UserEnvironment

    def get_queryset(self):
        self.environment = Environment.objects.get(pk=self.kwargs['env_pk'])

        rules_light.require(self.request.user, 'appstore.environment.update',
            self.environment)

        return UserEnvironment.objects.filter(environment=self.environment
            ).select_related('user')

    def get_context_data(self, object_list):
        return {
            'environment': self.environment,
            'userenvironment_list': object_list,
        }


class UserEnvironmentSecurityMixin(object):
    def get_object(self, queryset=None):
        obj = super(UserEnvironmentSecurityMixin, self).get_object(
            queryset)

        rules_light.require(self.request.user, 'appstore.environment.update',
            obj.environment)

        return obj

    def respond(self):
        runs = rules_light.run(self.request.user,
            'appstore.environment.update', self.object.environment)

        if runs:
            data = 'sucess'
        else:
            data = 'redirect'

        return http.HttpResponse(data, status=204)


class UserEnvironmentCreateView(generic.FormView):
    form_class = UserEnvironmentCreateForm
    model = UserEnvironment
    template_name = 'appstore/userenvironment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.environment = Environment.objects.get(pk=kwargs['env_pk'])

        rules_light.require(request.user, 'appstore.environment.update',
            self.environment)

        return super(UserEnvironmentCreateView, self).dispatch(request, *args,
            **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UserEnvironmentCreateView, self).get_form_kwargs()
        kwargs['environment'] = self.environment
        return kwargs

    def form_valid(self, form):
        site = get_current_site(self.request)

        mail_context = {
            'creator': self.request.user,
            'environment': self.environment,
            'site': site,
            'site_name': site.name,
            'site_domain': site.domain,
        }

        self.object = form.save(mail_context)

        return super(UserEnvironmentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserEnvironmentCreateView, self).get_context_data(
            **kwargs)
        context['environment'] = self.environment
        return context

    def get_success_url(self):
        return reverse('appstore_userenvironment_list',
                       args=(self.environment.pk,))


class UserEnvironmentDeleteView(UserEnvironmentSecurityMixin,
                                generic.DetailView):

    http_method_names = ['post']
    model = UserEnvironment

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.respond()


class UserEnvironmentUpdateView(UserEnvironmentSecurityMixin,
                                generic.DetailView):

    http_method_names = ['post']
    model = UserEnvironment

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_admin = request.POST['is_admin'] == u'1'
        self.object.save()
        return self.respond()


@rules_light.class_decorator
class EnvUpdateView(generic.UpdateView):
    """
    Update the environment.
    """
    form_class = EnvironmentForm
    model = Environment

    def get_success_url(self):
        """
        Back to the form again, but also reset the env cached in the session.
        """
        self.request.session['appstore_environment'] = self.object
        return self.request.path


class AppCategoryListView(generic.ListView):
    """
    List categories.
    """
    model = AppCategory


class AppCategoryDetailView(generic.DetailView):
    """
    List apps, filterable by tags, of a category.

    Also provide a list of categories for navigational purposes.
    """
    model = AppCategory

    def get_object(self, queryset=None):
        """
        Replace double dashes by a slash in the appcategory url kwarg.
        """
        return self.get_queryset().get(
            name=self.kwargs['appcategory'].replace('--', '/'))

    def get_context_data(self, **kwargs):
        """
        Add app_list, tag_list and appcategory_list to the context.
        """
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
    """
    Display details of an app on GET, take actions on the current env on post.
    """
    model = App

    def post(self, request, *args, **kwargs):
        """
        Take action with an app on the current environment on POST request.

        Supported actions are: 'install', 'uninstall', 'copy', 'update'.

        This is ment to be accessed via ajax.

        Install/uninstall: respond with 201 on success, 400 on failure.
        Copy/update: respond with 301 redirect to update view, 400 on failure.
        """
        environment = request.session['appstore_environment']

        rules_light.require(request.user, 'appstore.environment.update',
            environment)

        app = self.get_object()

        if request.user in environment.users.all():
            try:
                action = request.POST.get('action', None)

                if action == 'install':
                    environment.install(app)
                elif action == 'uninstall':
                    environment.uninstall(app)
                elif action == 'copy':
                    new_app = environment.copy(app)
                elif action == 'update':
                    new_app = environment.copy(app, True)
                else:
                    return http.HttpResponseBadRequest('Unknown action')

                if action in ('copy', 'update'):
                    return http.HttpResponseRedirect(reverse(
                        'appstore_app_update', args=(new_app.pk,)))
            except AppstoreException as e:
                return http.HttpResponseBadRequest(e.message)

            return http.HttpResponse(status=201)
        else:
            return http.HttpResponseForbidden('Not an admin for this env')


class AppCreateView(generic.CreateView):
    """
    Create an App using AppForm.
    """
    model = App
    form_class = AppForm

    def dispatch(self, request, *args, **kwargs):
        rules_light.require(request.user, 'appstore.environment.update',
            request.session['appstore_environment'])
        return super(AppCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Install the newly created App in the current environment.
        """
        result = super(AppCreateView, self).form_valid(form)
        self.request.session['appstore_environment'].install(self.object)
        return result

    def get_success_url(self):
        """
        Return the url to update the app.
        """
        return reverse('appstore_app_update', args=(self.object.pk,))


class AppUpdateView(generic.UpdateView):
    """
    Update an app.

    Note that the template extends ``appstore/app_base.html``, which checks
    App.editor. If App.editor is ``appstore.contrib.dummy_appeditor``, then it
    will include ``dummy_appeditor/links.html``.

    It is the role of the appeditor to provide actual functionnality.
    """
    model = App
    form_class = AppForm
    context_object_name = 'app'

    def get_object(self):
        """
        If the app is already deployed: edit it, and return the edit.
        """
        obj = super(AppUpdateView, self).get_object()

        if obj.deployed:
            raise CannotEditDeployedApp(obj)

        rules_light.require(self.request.user, 'appstore.app.update', obj)

        return obj

    def get_success_url(self):
        """ Return to the same URL """
        return self.request.path


class AppDeployView(generic.DetailView):
    """
    Deploy an App, to make it actually usable.
    """
    model = App
    template_name = 'appstore/app_deploy.html'

    def post(self, *args, **kwargs):
        """
        Set app.deployed=True and redirect to environment configuration url.
        """
        self.object = self.get_object()

        rules_light.require(self.request.user, 'appstore.app.deploy',
                            self.object)

        self.object.deployed = True
        self.object.save()

        if 'django.contrib.messages' in settings.INSTALLED_APPS:
            messages.add_message(self.request, messages.SUCCESS,
                _(u'App successfully deployed.'))

        return http.HttpResponseRedirect(reverse('appstore_env_update',
            args=[self.request.session['appstore_environment'].pk]))
