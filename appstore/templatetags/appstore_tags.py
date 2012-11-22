from django import template

register = template.Library()


@register.filter
def update_blocker(app, env):
    return env.update_blocker(app)
