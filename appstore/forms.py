from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.models import modelform_factory

import autocomplete_light
from autocomplete_light.contrib.taggit_tagfield import TagField, TagWidget

from settings import EDITOR_MODULES
from models import Environment, App, AppCategory


class AppFormBase(autocomplete_light.FixedModelForm):
    tags = TagField(widget=TagWidget('TagAutocomplete'))

    class Meta:
        model = App


class AppForm(autocomplete_light.FixedModelForm):
    class Meta:
        fields = ('name', 'description', 'editor', 'provides')
        model = App


class EnvironmentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']

        if not len(name.strip()):
            raise forms.ValidationError(_(u'Name must not be blank'))

        return name

    class Meta:
        model = Environment
        fields = ('name',)
