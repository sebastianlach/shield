from django import forms

from .models import File, Link, Reference


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['content', ]


class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ['url', ]


class LinkFileForm(forms.Form):
    url = forms.URLField(required=False)
    content = forms.FileField(required=False)

    def clean(self):
        url = self.cleaned_data.get('url')
        content = self.cleaned_data.get('content')

        if not url and not content:
            raise forms.ValidationError('One of fields is required')

        if url and content:
            raise forms.ValidationError('Provide only one field.')

        return self.cleaned_data


class ReferenceCheckForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = Reference
        fields = ['password', ]
