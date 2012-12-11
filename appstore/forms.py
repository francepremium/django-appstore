import string
from random import choice

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from django.template.loader import render_to_string
from django.core.mail import send_mail

import autocomplete_light
from autocomplete_light.contrib.taggit_tagfield import TagField, TagWidget

from settings import EDITOR_MODULES
from models import Environment, App, AppCategory, UserEnvironment


class AppFormBase(autocomplete_light.FixedModelForm):
    tags = TagField(widget=TagWidget('TagAutocomplete'))

    class Meta:
        model = App


class AppForm(autocomplete_light.FixedModelForm):
    def __init__(self, *args, **kwargs):
        super(AppForm, self).__init__(*args, **kwargs)
        self.fields['editor'].initial = self.fields['editor'].choices[1][0]
        default_feature = self.fields['provides'].queryset[0].pk
        self.fields['provides'].initial = default_feature

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


class UserEnvironmentCreateForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    is_admin = forms.BooleanField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        exists = UserEnvironment.objects.filter(user__email=email,
            environment=self.environment).count()

        if exists:
            raise forms.ValidationError(
                _(u'This user is already in your environment'))

        return email

    def __init__(self, environment, *args, **kwargs):
        self.environment = environment
        super(UserEnvironmentCreateForm, self).__init__(*args, **kwargs)

    def save(self, mail_context):
        user, created = User.objects.get_or_create(
            email=self.cleaned_data['email'],
            username=self.cleaned_data['email'])
        userenvironment = UserEnvironment(user=user,
            environment=self.environment,
            is_admin=self.cleaned_data.get('is_admin', False))

        mail_context['user'] = user
        mail_context.setdefault('environment_url',
                self.environment.get_absolute_url())

        if created:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            userenvironment.default = True

            password = ''.join(
                [choice(string.letters + string.digits) for i in range(7)])
            user.set_password(password)
            mail_context['password'] = password

            mail_template = 'appstore/user_created_notification_message.txt'
        else:
            mail_template = \
                'appstore/environment_open_notification_message.txt'

        s = u'%(creator)s invited you to join %(environment)s on %(site_name)s'
        subject = _(s)
        subject = subject % mail_context
        message = render_to_string(mail_template, mail_context)

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
            [user.email])

        user.save()
        userenvironment.save()
        return userenvironment
