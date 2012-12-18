import rules_light


rules_light.registry['form_designer.form.create'] = False


@rules_light.is_authenticated
def update_form(user, rule, form):
    return rules_light.registry.run(user, 'appstore.app.update',
        form.appform.app)


rules_light.registry['form_designer.form.update'] = update_form
