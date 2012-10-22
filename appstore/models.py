from django.db import models
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from signals import post_app_install, post_app_uninstall
from exceptions import (AppAlreadyInstalled, AppVersionNotInstalled,
        CannotUninstallDependency)


class AppCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='appstore/appcategory/logo')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        name = self.name.replace('/', '--')
        return reverse('appstore_appcategory_detail', args=[name])

    class Meta:
        ordering = ('name',)


class AppFeature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class App(models.Model):
    category = models.ForeignKey(AppCategory)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='appstore/app/image')
    provides = models.ForeignKey(AppFeature)
    default_for_feature = models.BooleanField()
    in_appstore = models.BooleanField()
    fork_of = models.ForeignKey('self', related_name='fork_set',
            null=True, blank=True)
    tags = TaggableManager(blank=True)

    @property
    def last_appversion(self):
        return self.appversion_set.order_by('-version')[0]

    def get_absolute_url(self):
        return reverse('appstore_app_detail', args=[self.pk])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class AppVersion(models.Model):
    app = models.ForeignKey(App)
    version = models.IntegerField()
    requires = models.ManyToManyField(AppFeature, blank=True)
    author = models.ForeignKey('auth.user')
    fork_of = models.ForeignKey('self', related_name='fork_set',
            null=True, blank=True)

    def __unicode__(self):
        return u'%s v%s' % (self.app, self.version)

    class Meta:
        ordering = ('app', 'version')

    def get_required_by(self, env):
        return env.appversions.exclude(pk=self.pk).filter(
            requires=self.app.provides)

    def fork(self, author):
        app_fork = App(category=self.app.category, name=self.app.name,
                description=self.app.description, image=self.app.image,
                provides=self.app.provides, fork_of=self.app)
        app_fork.save()
        appversion_fork = AppVersion(app=app_fork, version=self.version,
                fork_of=self, author=author)
        appversion_fork.save()

        for appfeature in self.requires.all():
            appversion_fork.requires.add(appfeature)

        return appversion_fork


class Environment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    appversions = models.ManyToManyField(AppVersion)
    users = models.ManyToManyField('auth.user')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    @property
    def installed_apps(self):
        return App.objects.filter(appversion__in=self.appversions.all())

    @property
    def appfeatures(self):
        return AppFeature.objects.filter(app__in=self.installed_apps)

    def install_app(self, app):
        appversion = app.last_appversion
        self.install_appversion(appversion)
        return appversion

    def install_appversion(self, appversion):
        if appversion.app in self.installed_apps:
            raise AppAlreadyInstalled(self, appversion)

        for appfeature in appversion.requires.all():
            if appfeature in self.appfeatures:
                continue

            requirement = App.objects.get(default_for_feature=True,
                provides=appfeature)
            self.install_app(requirement)

        self.appversions.add(appversion)
        return post_app_install.send(sender=self, appversion=appversion)

    def uninstall_app(self, app):
        appversion = self.appversions.get(app=app)
        self.uninstall_appversion(appversion)
        return appversion

    def uninstall_appversion(self, appversion):
        required_by = appversion.get_required_by(self)
        if required_by:
            raise CannotUninstallDependency(self, appversion,
                required_by[0])

        if appversion not in self.appversions.all():
            raise AppVersionNotInstalled(self, appversion)

        self.appversions.remove(appversion)
        return post_app_uninstall.send(sender=self, appversion=appversion)
