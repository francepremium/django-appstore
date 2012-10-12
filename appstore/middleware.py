class EnvironmentMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        environments = request.user.environment_set.all()

        if not environments:
            env = request.user.environment_set.create(name=request.user.email)
        elif 'appstore_environment' in request.session.keys():
            env = request.session['appstore_environment']
        else:
            env = environments[0]

        request.session['appstore_environment'] = env
