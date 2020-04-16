from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseGone,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from rest_framework import viewsets
from rest_framework.response import Response

from .forms import FileForm, LinkForm, LinkFileForm, ReferenceCheckForm
from .helpers import generate_token, token_hash
from .models import File, Link, Reference, Redirect


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Main view with form for adding references.
    """
    template_name = "index.html"

    def get(self, request):
        form = LinkFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        token = None
        reference = None

        form = LinkFileForm(request.POST, request.FILES)
        if form.is_valid():

            token = generate_token()

            if form.cleaned_data['url']:
                link_form = LinkForm(request.POST)
                link_form.instance.user = request.user
                entity = link_form.save()
                reference = Reference()
                reference.user = request.user
                reference.entity = entity
                reference.token = token_hash(token)
                reference.save()

            if form.cleaned_data['content']:
                file_form = FileForm(request.POST, request.FILES)
                file_form.instance.user = request.user
                entity = file_form.save()
                reference = Reference()
                reference.user = request.user
                reference.entity = entity
                reference.token = token_hash(token)
                reference.save()

        context = dict(
            form=form,
            token=token,
            reference=reference,
        )
        return render(request, self.template_name, context)


class LinkListView(LoginRequiredMixin, ListView):
    """
    View that lists links.
    """
    model = Link
    template_name = 'links/list.html'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class FileListView(LoginRequiredMixin, ListView):
    """
    View that lists files.
    """
    model = File
    template_name = 'files/list.html'

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)


class ReferenceListView(LoginRequiredMixin, ListView):
    """"
    View that list references.
    """
    model = Reference
    template_name = 'references/list.html'

    def get_queryset(self):
        return Reference.objects.filter(user=self.request.user)


class ReferenceCheckView(View):
    """
    View which checks password of reference.
    """
    model = Reference
    form_class = ReferenceCheckForm
    template_name = 'references/check.html'

    def get(self, request, rid):
        reference = self.model.objects.get(rid=rid)
        if reference.expired:
            return HttpResponseGone()

        form = self.form_class(instance=reference)
        return render(request, self.template_name, {'form': form})

    def post(self, request, rid, *args, **kwargs):
        reference = self.model.objects.get(rid=rid)
        if reference.expired:
            return HttpResponseGone()

        form = self.form_class(request.POST)
        if form.is_valid():
            if reference.token != token_hash(form.cleaned_data['password']):
                form.add_error(None, 'Invalid password')
            else:
                redirect = Redirect()
                redirect.user = request.user
                redirect.reference = reference
                redirect.save()
                return HttpResponseRedirect(reference.url)

        return render(request, self.template_name, {'form': form})
