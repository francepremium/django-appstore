class AppstoreException(Exception):
    """ Parent class for all exceptions of this class. """
    pass


class AppAlreadyInstalled(AppstoreException):
    """
    Raised by Environment.install when trying to install an already
    installed app.
    """
    def __init__(self, env, appversion):
        super(AppAlreadyInstalled, self).__init__(
            'Cannot install %s because %s is already installed in env %s' % (
                appversion, env.appversions.filter(app=appversion.app), env))


class AppVersionNotInstalled(AppstoreException):
    """
    Raised by Environment.uninstall when trying to uninstall an AppVersion that
    is not installed.
    """
    def __init__(self, env, appversion):
        super(AppVersionNotInstalled, self).__init__(
            'Cannot uninstall %s from env %s because it is not installed' % (
                appversion, env))


class CannotUninstallDependency(AppstoreException):
    """
    Raised by Environment.uninstall when trying to uninstall an AppVersion
    which is a dependency of another installed AppVersion.
    """
    def __init__(self, env, appversion, parent):
        super(CannotUninstallDependency, self).__init__(
            'Cannot uninstall %s from %s because %s depends on it' % (
                appversion, env, parent))
