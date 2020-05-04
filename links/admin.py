from django.contrib import admin

from .helpers import token_hash
from .models import File, Link, Reference, Redirect, UserAgent


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['token'] != form.base_fields['token'].initial:
            obj.token = token_hash(form.cleaned_data['token'])
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['token'].initial = obj.token if obj else ''
        return form


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    pass
