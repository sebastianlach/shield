from django.forms import ModelForm, CharField

from .models import File, Link, Reference


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'content']


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ['name', 'url']


class ReferenceCheckForm(ModelForm):
    password = CharField()

    class Meta:
        model = Reference
        fields = ['password', ]
