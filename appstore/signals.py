from django import dispatch


post_app_install = dispatch.Signal(providing_args=['appversion'])
post_app_uninstall = dispatch.Signal(providing_args=['appversion'])
