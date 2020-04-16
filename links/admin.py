from django.contrib import admin

from .models import File, Link, Reference, Redirect, UserAgent


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    pass
