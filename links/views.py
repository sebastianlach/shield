from datetime import datetime
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, ListView, TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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
            return HttpResponseNotFound()

        form = self.form_class(instance=reference)
        return render(request, self.template_name, {'form': form})

    def post(self, request, rid, *args, **kwargs):
        reference = self.model.objects.get(rid=rid)
        if reference.expired:
            return HttpResponseNotFound()

        form = self.form_class(request.POST)
        if form.is_valid():
            if reference.token != token_hash(form.cleaned_data['password']):
                form.add_error(None, 'Invalid password')
            else:
                redirect = Redirect()
                redirect.reference = reference
                redirect.save()
                return HttpResponseRedirect(reference.url)

        return render(request, self.template_name, {'form': form})


class ReferencesView(APIView):
    """
    API endpoint for adding new links/files.
    """

    def post(self, request, format=None):
        token = None

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

        else:
            return Response(
                {'errors': dict(form.errors.items())},
                status=status.HTTP_400_BAD_REQUEST
            )

        context = dict(
            token=token,
            url=reverse('api_reference', args=[reference.rid]),
        )
        return Response(context)


class ReferenceView(APIView):
    """
    API endpoint for accessing links/files.
    """
    permission_classes = [AllowAny]

    def post(self, request, rid, format=None):
        reference = Reference.objects.get(rid=rid)
        if reference.expired:
            return Response(
                {'errors': 'reference expired'},
                status=status.HTTP_404_NOT_FOUND
            )

        form = ReferenceCheckForm(request.POST)
        if form.is_valid():
            if reference.token == token_hash(form.cleaned_data['password']):
                redirect = Redirect()
                redirect.reference = reference
                redirect.save()
                return HttpResponseRedirect(reference.url)
            else:
                return Response(
                    {'errors': 'invalid password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {'errors': dict(form.errors.items())},
                status=status.HTTP_400_BAD_REQUEST
            )


class StatisticsView(APIView):
    """
    API endpoint for statistics.
    """

    def get(self, request, format=None):
        link_type = ContentType.objects.get(app_label='links', model='link')
        file_type = ContentType.objects.get(app_label='links', model='file')

        references = Reference.objects.filter(user=self.request.user)\
            .prefetch_related('redirects')

        stats = defaultdict(lambda: dict(files=0, links=0))
        for reference in references:
            if len(reference.redirects.all()):
                index = reference.timestamp.strftime('%Y-%m-%d')
                if reference.entity_type == file_type:
                    stats[index]['files'] += 1
                if reference.entity_type == link_type:
                    stats[index]['links'] += 1

        return Response(stats)
