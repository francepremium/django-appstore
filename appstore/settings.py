from django.conf import settings


EDITOR_MODULES = getattr(settings, 'APPSTORE_EDITOR_MODULES',
    [])
