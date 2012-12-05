import copy

from django.db import models
from django.db.models import signals

from form_designer.models import Form
from appstore.models import App
from appstore.signals import post_app_copy


class AppForm(models.Model):
    app = models.OneToOneField('appstore.app')
    form = models.OneToOneField('form_designer.form')

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


def copy_form(sender, source_app, new_app, **kwargs):
    for tab in source_app.appform.form.tab_set.all():
        new_tab = copy.deepcopy(tab)
        new_tab.pk = None
        new_tab.form = new_app.appform.form
        new_tab.save()

        for widget in tab.widget_set.all().select_subclasses():
            widget.pk = None
            widget.id = None
            widget.tab = new_tab
            widget.save()
post_app_copy.connect(copy_form)
