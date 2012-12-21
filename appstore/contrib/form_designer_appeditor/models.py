import copy

from django.db.models import Count
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

    form = Form.objects.create(author=instance.author,
                               verbose_name=instance.name)
    AppForm(app=instance, form=form).save()
signals.post_save.connect(auto_appform, sender=App)


def copy_form(sender, source_app, new_app, **kwargs):
    if source_app.editor != 'appstore.contrib.form_designer_appeditor':
        return

    new_app.appform.form.verbose_name = source_app.appform.form.verbose_name
    new_app.appform.form.author = source_app.appform.form.author

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

    empty = new_app.appform.form.tab_set.annotate(widget_count=Count('widget')
            ).filter(widget_count=0)

    if empty.count() == new_app.appform.form.tab_set.all().count():
        empty.exclude(pk=new_app.appform.form.tab_set.all()[0].pk).delete()
    else:
        empty.delete()
post_app_copy.connect(copy_form)
