from django.contrib.auth.models import User

from models import UserEnvironment

from rules_light import *


@is_authenticated
def is_staff_or_admin_of_environment(user, rule, environment):
    if not isinstance(user, User):
        return False

    if user.is_staff:
        return True

    try:
        user_environment = UserEnvironment.objects.get(user=user.pk,
            environment=environment.pk)
    except UserEnvironment.DoesNotExist:
        return False

    return user_environment.is_admin

registry['appstore.environment.create'] = is_authenticated
registry['appstore.environment.update'] = is_staff_or_admin_of_environment
registry['appstore.environment.delete'] = is_staff_or_admin_of_environment


@is_authenticated
def has_access_or_staff(user, rule, env):
    if user.is_staff:
        return True

    try:
        UserEnvironment.objects.get(user=user, environment=env)
    except UserEnvironment.DoesNotExist:
        return False
    else:
        return True
registry['appstore.environment.read'] = has_access_or_staff


@is_authenticated
def staff_or_admin_of_environments(user, rule, app):
    if user.is_staff:
        return True

    for environment in app.environment_set.all():
        if not environment.is_admin(user):
            return False

    return True
registry['appstore.app.update'] = staff_or_admin_of_environments
registry['appstore.app.deploy'] = staff_or_admin_of_environments
