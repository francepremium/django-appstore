from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from signals import post_app_install, post_app_uninstall
from exceptions import AppAlreadyInstalled, AppVersionNotInstalled, CannotUninstallDependency


class AppCategory(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='appstore/appcategory/logo')

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class App(models.Model):
    category = models.ForeignKey(AppCategory)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='appstore/app/image')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class AppVersion(models.Model):
    app = models.ForeignKey(App)
    version = models.IntegerField()
    dependencies = models.ManyToManyField(App, related_name='required_by')
    public = models.BooleanField()
    fork_of = models.ForeignKey('self', related_name='fork_set',
            null=True, blank=True)
    author = models.ForeignKey('auth.user')

    def __unicode__(self):
        return u'%s v%s' % (self.app, self.version)

    class Meta:
        ordering = ('app', 'version')

    def fork(self, author):
        fork = AppVersion(app=self.app, version=self.version, public=False,
                fork_of=self, author=author)
        fork.save()

        for dependency in self.dependencies.all():
            fork.dependencies.add(dependency)

        return fork


class Environment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    appversions = models.ManyToManyField(AppVersion)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    @property
    def installed_apps(self):
        return App.objects.filter(appversion__in=self.appversions.all())

    def install_app(self, app):
        appversion = app.appversion_set.order_by('-version')[0]
        self.install_appversion(appversion)
        return appversion

    def install_appversion(self, appversion):
        if appversion.app in self.installed_apps:
            raise AppAlreadyInstalled(self, appversion)

        dependencies = appversion.dependencies.all()

        while dependencies:
            for dependency in dependencies:
                dependency_appversion = self.install_app(dependency)
            dependencies = dependency_appversion.dependencies.all()

        self.appversions.add(appversion)
        post_app_install.send(sender=self, appversion=appversion)

    def uninstall_appversion(self, appversion):
        for installed_appversion in self.appversions.all():
            if appversion.app in installed_appversion.dependencies.all():
                raise CannotUninstallDependency(self, appversion,
                    installed_appversion)

        if appversion not in self.appversions.all():
            raise AppVersionNotInstalled(self, appversion)

        self.appversions.remove(appversion)
        post_app_uninstall.send(sender=self, appversion=appversion)
