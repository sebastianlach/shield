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
from .models import File, Link, Reference
from .serializers import (
    LinkSerializer,
    FileSerializer,
    ReferenceSerializer,
)


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Index view.
    """
    template_name = "index.html"

    def get(self, request):
        form = LinkFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        token = None
        entity = None

        form = LinkFileForm(request.POST, request.FILES)
        if form.is_valid():

            token = generate_token()

            if form.cleaned_data['url']:
                link_form = LinkForm(request.POST)
                entity = link_form.save()
                reference = Reference()
                reference.entity = entity
                reference.token = token_hash(token)
                reference.save()

            if form.cleaned_data['content']:
                file_form = FileForm(request.POST, request.FILES)
                entity = file_form.save()
                reference = Reference()
                reference.entity = entity
                reference.token = token_hash(token)
                reference.save()

        context = dict(
            form=form,
            token=token,
            reference=reference,
        )
        return render(request, self.template_name, context)


class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that handles links.
    """
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that handles files.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer


class StatisticsViewSet(viewsets.ViewSet):
    """
    API endpoint that provides statistics.
    """
    queryset = Reference.objects.all()

    def list(self, request):
        statistics = dict()

        for ref in self.queryset:
            index = self.reference_index(ref)
            statistics.setdefault(index, dict(Link=0, File=0))
            statistics[index][ref.entity.__class__.__name__] += 1

        return Response(statistics)

    def reference_index(self, ref):
        return ref.entity.created_at.strftime('%Y-%m-%d')


class LinkListView(LoginRequiredMixin, ListView):
    """
    API endpoint that lists links.
    """
    model = Link
    template_name = 'links/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class FileListView(LoginRequiredMixin, ListView):
    """
    API endpoint that lists files.
    """
    model = File
    template_name = 'files/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReferenceListView(LoginRequiredMixin, ListView):
    """"
    API endpoint that list references.
    """
    model = Reference
    template_name = 'references/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReferenceCheckView(View):
    """
    Reference check view.
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
                return HttpResponseRedirect(reference.url)

        return render(request, self.template_name, {'form': form})
