from django.views import generic

from models import DummyApp
from forms import DummyAppForm


class DummyAppUpdateView(generic.UpdateView):
    model = DummyApp
    form_class = DummyAppForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *args, **kwargs):
        context = super(DummyAppUpdateView, self).get_context_data(*args, **kwargs)
        context['app'] = self.object.app
        return context
