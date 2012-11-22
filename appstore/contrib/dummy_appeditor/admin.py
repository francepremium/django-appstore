from django.contrib import admin

from models import DummyApp


class DummyAppAdmin(admin.ModelAdmin):
    list_display = ('app', 'sound')
    list_editable = ('sound',)
admin.site.register(DummyApp, DummyAppAdmin)
