from django.utils.translation import ugettext_lazy as _


class AppstoreException(Exception):
    """ Parent class for all exceptions of this class. """
    pass


class AppAlreadyInstalled(AppstoreException):
    """
    Raised by Environment.install when trying to install an already
    installed app.
    """
    def __init__(self, env, app):
        super(AppAlreadyInstalled, self).__init__(
            _(u'%(app)s is already installed in environment %(env)s') %
            {'app': app, 'env': env})


class AppNotInstalled(AppstoreException):
    """
    Raised by Environment.uninstall when trying to uninstall an App that
    is not installed.
    """
    def __init__(self, env, app):
        super(AppNotInstalled, self).__init__(
            u'Cannot uninstall %s from env %s because it is not installed' % (
                app, env))


class CannotUninstallDependency(AppstoreException):
    """
    Raised by Environment.uninstall when trying to uninstall an AppVersion
    which is a dependency of another installed AppVersion.
    """
    def __init__(self, env, app, required_by):
        super(CannotUninstallDependency, self).__init__(
            _(u'Cannot uninstall %(app)s from %(env)s because %(required_by)s depends on it') %
            {'app': app, 'env': env, 'required_by': required_by})


class CannotEditDeployedApp(AppstoreException):
    """
    Raised by AppUpdateView before updating an App that is already deployed.
    """
    def __init__(self, app):
        super(CannotEditDeployedApp, self).__init__(
            _(u'Cannot update %s because it is already deployed') % app)


class UpdateAlreadyPendingDeployment(AppstoreException):
    """
    Raised when trying to create a superseed copy when another one already
    exists.
    """
    def __init__(self, env, source_app, blocking_app):
        msg = u' '.join((
            unicode(_(u'Another update is already pending for deployment.')),
            unicode(
                _(u'Uninstall it or deploy it before creating a new update')),
        ))

        super(UpdateAlreadyPendingDeployment, self).__init__(msg)


class CannotUpdateNonDeployedApp(AppstoreException):
    def __init__(self, app):
        super(CannotUpdateNonDeployedApp, self).__init__(
            u'Cannot create update for non deployed app "%s"' % app)


class CannotRemoveLastAdmin(AppstoreException):
    def __init__(self, env):
        super(CannotRemoveLastAdmin, self).__init__(
            u'Cannot remove the last admin of environment "%s"' % env)
