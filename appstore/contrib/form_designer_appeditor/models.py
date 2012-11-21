from django.db import models
from django.db.models import signals

from form_designer.models import Form
from appstore.models import App


class AppForm(models.Model):
    app = models.ForeignKey('appstore.app')
    form = models.ForeignKey('form_designer.form')

    def __unicode__(self):
        return u'Form for %s' % self.app


def auto_appform(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.editor != 'appstore.contrib.form_designer_appeditor':
        return

    form = Form.objects.create(author_id=1, verbose_name=instance.name)
    AppForm(app=instance, form=form).save()
signals.post_save.connect(auto_appform, sender=App)
