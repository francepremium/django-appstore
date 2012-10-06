from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from signals import post_app_install, post_app_uninstall
from exceptions import AppAlreadyInstalled, AppVersionNotInstalled


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
    dependencies = models.ManyToManyField('self', related_name='required_by', symmetrical=False)

    def __unicode__(self):
        return u'%s v%s' % (self.app, self.version)

    class Meta:
        ordering = ('app', 'version')


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

    def install(self, appversion):
        if appversion.app in self.installed_apps:
            raise AppAlreadyInstalled(self, appversion)

        dependencies = appversion.dependencies.all()

        while dependencies:
            for dependency in dependencies:
                self.install(dependency)
            dependencies = dependency.dependencies.all()

        self.appversions.add(appversion)
        post_app_install.send(sender=self, appversion=appversion)

    def uninstall(self, appversion):
        self.appversions.remove(appversion)
        post_app_uninstall.send(sender=self, appversion=appversion)
