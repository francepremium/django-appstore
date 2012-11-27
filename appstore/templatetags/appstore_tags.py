from django import template

register = template.Library()


@register.filter
def update_blocker(app, env):
    if not env:
        return True
    return env.update_blocker(app)
