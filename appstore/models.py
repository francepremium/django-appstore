from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from settings import EDITOR_MODULES
from signals import post_app_install, post_app_uninstall, post_app_copy
from exceptions import (AppAlreadyInstalled, AppNotInstalled,
        CannotUninstallDependency, UpdateAlreadyPendingDeployment)


class AppCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True,
            upload_to='appstore/appcategory/logo')

    def __unicode__(self):
        return self.name

    def get_absolute_update_url(self):
        return reverse('appstore_appcategory_update', args=(self.pk,))

    def get_absolute_url(self):
        name = self.name.replace('/', '--')
        return reverse('appstore_appcategory_detail', args=[name])

    class Meta:
        ordering = ('name',)


class AppFeature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def get_absolute_update_url(self):
        return reverse('appstore_appfeature_update', args=(self.pk,))

    @property
    def default_app(self):
        return self.provided_by.get(default_for_feature=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class App(models.Model):
    # Cosmetics
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='appstore/app/image')
    category = models.ForeignKey(AppCategory, null=True, blank=True)
    tags = TaggableManager(blank=True)
    in_appstore = models.BooleanField()

    provides = models.ForeignKey(AppFeature, null=True, blank=True,
        related_name='provided_by')
    requires = models.ManyToManyField(AppFeature, blank=True,
        related_name='required_by')
    default_for_feature = models.BooleanField()

    superseeds = models.ForeignKey('self', related_name='superseeded_by', null=True,
        blank=True)
    deployed = models.BooleanField()

    editor = models.CharField(null=True, blank=True, choices=EDITOR_MODULES,
        max_length=100)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ''

    @property
    def editor_module_name(self):
        return self.editor.split('.')[-1]

    def get_absolute_url(self):
        return reverse('appstore_app_detail', args=[self.pk])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


def deploy_superseeds_mark_dirty(sender, instance, **kwargs):
    """
    Check if .deployed changed, if so, set instance._updating = True.

    This will be picked up by deploy_superseeds_apply.
    """
    if not instance.pk:
        return

    if not instance.deployed:
        return

    if not instance.superseeds_id:
        return

    try:
        actual = App.objects.get(pk=instance.pk)
    except App.DoesNotExist:
        return  # probably created from loaddata
    else:
        if not actual.deployed:
            instance._updating = True
signals.pre_save.connect(deploy_superseeds_mark_dirty, sender=App)


def deploy_superseeds_apply(sender, instance, created, **kwargs):
    """
    Deploying an app superseeds the app it is based on, if any.

    If a user edits App "foo", then App "foo" should remain installed until the
    edit is deployed.

    When the edit is deployed, it's parent can be uninstalled.
    """
    if created:
        return

    if getattr(instance, '_updating', False):
        for environment in instance.environment_set.all():
            environment.uninstall(instance.superseeds)
signals.post_save.connect(deploy_superseeds_apply, sender=App)


class Environment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    apps = models.ManyToManyField('appstore.app')
    users = models.ManyToManyField('auth.user')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def install(self, app):
        if app in self.apps.all():
            raise AppAlreadyInstalled(self, app)

        # install the default app for each feature, if another installed app
        # doesn't already provide it
        for feature in app.requires.exclude(provided_by__in=self.apps.all()):
            self.install(feature.default_app)

        self.apps.add(app)
        post_app_install.send(sender=self, app=app)

    def uninstall(self, app):
        if app not in self.apps.all():
            raise AppNotInstalled(self, app)

        # are there any other apps that provide the same feature ?
        has_alternative = AppFeature.objects.filter(pk=app.provides.pk,
            provided_by__in=self.apps.exclude(pk=app.pk))

        # if no other app provides the same feature as app
        if not has_alternative:
            # check if that feature is necessary
            requirements = AppFeature.objects.filter(
                required_by=self.apps.exclude(pk=app.pk))

            if app.provides in requirements:
                # in that case find what apps require it, and fail
                blockers = self.apps.filter(requires=app.provides)
                raise CannotUninstallDependency(self, app, blockers)

        self.apps.remove(app)
        post_app_uninstall.send(sender=self, app=app)

    def copy(self, app, superseed=False):
        if superseed:
            blocker = App.objects.filter(environment=self, superseeds=app,
                deployed=False)

            if blocker:
                raise UpdateAlreadyPendingDeployment(self, app, blocker[0])

        new_app = App(
            name=app.name,
            description=app.description,
            image=app.image,
            category=app.category,
            provides=app.provides,
            editor=app.editor,
        )

        if superseed:
            new_app.superseeds = app

        new_app.save()

        for requirement in app.requires.all():
            new_app.requires.add(requirement)

        self.install(new_app)

        post_app_copy.send(sender=self, source_app=app, new_app=new_app)

        return new_app
