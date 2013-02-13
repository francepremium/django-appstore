from django.contrib import admin

from models import AppFeature, AppCategory, App, Environment


class AppCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(AppCategory, AppCategoryAdmin)


class AppFeatureAdmin(admin.ModelAdmin):
    pass
admin.site.register(AppFeature, AppFeatureAdmin)


class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'provides', 'image',
            'default_for_feature', 'in_appstore', 'editor')
    list_editable = ('category', 'provides',
            'default_for_feature', 'in_appstore', 'editor')
admin.site.register(App, AppAdmin)


class EnvironmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Environment, EnvironmentAdmin)


import hyperadmin
from hyperadmin.resources.models import ModelResource, InlineModelResource

class AppResource(InlineModelResource):
    model = App

class AppCategoryResource(ModelResource):
    inlines = [AppResource]
    list_display = ['name']

hyperadmin.site.register(AppCategory, AppCategoryResource)

