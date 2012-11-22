from django.db import models
from django.db.models import signals

from appstore.models import App
from appstore.signals import post_app_copy


class DummyApp(models.Model):
    app = models.OneToOneField('appstore.app')
    sound = models.TextField()

    def __unicode__(self):
        return u'Sound for %s' % self.app


def auto_dummyapp(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.editor != 'appstore.contrib.dummy_app':
        return

    DummyApp(app=instance).save()
signals.post_save.connect(auto_dummyapp, sender=App)


def copy_dummyapp(sender, source_app, new_app, **kwargs):
    if new_app.editor != 'appstore.contrib.dummy_app':
        return

    DummyApp(app=new_app, sound=source_app.dummyapp.sound).save()
post_app_copy.connect(copy_dummyapp)
