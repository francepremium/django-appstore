from django.contrib import admin

from models import AppFeature, AppCategory, App, AppVersion, Environment


class AppCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(AppCategory, AppCategoryAdmin)


class AppFeatureAdmin(admin.ModelAdmin):
    pass
admin.site.register(AppFeature, AppFeatureAdmin)

class AppAdmin(admin.ModelAdmin):
    pass
admin.site.register(App, AppAdmin)


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('app', 'version', 'public', 'fork_of', 'dependency_list',
        'author')

    def dependency_list(self, obj):
        return u', '.join(obj.dependencies.values_list('name', flat=True))

    list_editable = ('public',)
admin.site.register(AppVersion, AppVersionAdmin)


class EnvironmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Environment, EnvironmentAdmin)
