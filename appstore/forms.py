from django import forms

from models import Environment


class EnvironmentForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ('name',)
