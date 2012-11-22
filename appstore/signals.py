"""
Signals for this app are: post_app_install, post_app_uninstall, post_app_copy.

post_app_install, post_app_uninstall
    Sent when an app is installed or uninstalled from an environment, with
    sender=environment, and app=the app.

post_app_copy
    Sent when an app is copied, with sender=environment, source_app=the app
    that is copied and new_app=the new, freshly copied app.
"""

from django import dispatch

__all__ = ('post_app_install', 'post_app_uninstall', 'post_app_copy')

post_app_install = dispatch.Signal(providing_args=['app'])
post_app_uninstall = dispatch.Signal(providing_args=['app'])
post_app_copy = dispatch.Signal(providing_args=['source_app', 'new_app'])
