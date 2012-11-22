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
        if not request.user.is_authenticated():
            return

        if 'appstore_environment' in request.session.keys():
            return

        try:
            user_env = UserEnvironment.objects.get(user=request.user,
                default=True)
        except UserEnvironment.DoesNotExist:
            env = Environment(name=request.user.email)
            env.save()
            UserEnvironment(environment=env, user=request.user,
                    is_admin=True).save()
            request.session['appstore_environment'] = env
        else:
            request.session['appstore_environment'] = user_env.environment
