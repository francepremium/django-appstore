from django.conf import settings
from django import http

from models import Environment, UserEnvironment


class EnvironmentMiddleware(object):
    """
    Set request.session['appstore_environment'] at all cost.

    Set request.session['appstore_environment'] to the default environment it
    has if any.

    Else create a default environment for this user and set
    request.session['appstore_environment'].
    """
    def process_request(self, request):
        if settings.STATIC_URL in request.path:
            return

        if not request.user.is_authenticated():
            return

        if 'appstore_environment' in request.session.keys():
            try:
                UserEnvironment.objects.get(user=request.user,
                    environment=request.session['appstore_environment'])
            except UserEnvironment.DoesNotExist:
                env = UserEnvironment.objects.filter(user=request.user
                    )[0].environment
                request.session['appstore_environment'] = env
                # todo: message
                return http.HttpResponseRedirect('/')
            return

        try:
            user_env = UserEnvironment.objects.get(user=request.user,
                default=True)
        except UserEnvironment.DoesNotExist:
            env, c = Environment.objects.get_or_create(name=request.user.email)
            UserEnvironment(environment=env, user=request.user,
                    is_admin=True).save()
            request.session['appstore_environment'] = env
        else:
            request.session['appstore_environment'] = user_env.environment
