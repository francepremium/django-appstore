from django.contrib import admin

from models import AppFeature, AppCategory, App, AppVersion, Environment


class AppCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(AppCategory, AppCategoryAdmin)


class AppFeatureAdmin(admin.ModelAdmin):
    pass
admin.site.register(AppFeature, AppFeatureAdmin)

class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'provides', 'image',
            'default_for_feature', 'fork_of', 'in_appstore')
    list_editable = ('category', 'provides',
            'default_for_feature', 'in_appstore')
admin.site.register(App, AppAdmin)


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('app', 'version', 'fork_of',
        'author')
admin.site.register(AppVersion, AppVersionAdmin)


class EnvironmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Environment, EnvironmentAdmin)
