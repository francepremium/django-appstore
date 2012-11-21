from form_designer.views import FormUpdateView

from models import AppForm


class AppFormUpdateView(FormUpdateView):
    def get_object(self):
        self.appform = AppForm.objects.get(app__pk=self.kwargs['app_pk'])
        return self.appform.form

    def get_context_data(self, **kwargs):
        context = super(AppFormUpdateView, self).get_context_data()
        context['app'] = self.appform.app
        context['appform'] = self.appform
        return context
