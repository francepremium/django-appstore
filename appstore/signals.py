from django import dispatch


post_app_install = dispatch.Signal(providing_args=['app'])
post_app_uninstall = dispatch.Signal(providing_args=['app'])
post_app_edit = dispatch.Signal(providing_args=['app'])
