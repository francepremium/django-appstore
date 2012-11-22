from django import forms

from models import DummyApp


class DummyAppForm(forms.ModelForm):
    class Meta:
        model = DummyApp
        exclude = ('app',)
