from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.utils import timezone

from .helpers import bitwise_or


RESOURCES = (
    models.Q(app_label='links', model='file'),
    models.Q(app_label='links', model='link'),
)


class Reference(models.Model):
    """Reference model."""
    rid = models.UUIDField(default=uuid4, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=32)
    entity_id = models.PositiveIntegerField()
    entity_type = models.ForeignKey(
        ContentType,
        limit_choices_to=bitwise_or(RESOURCES),
        on_delete=models.CASCADE,
    )
    entity = GenericForeignKey('entity_type', 'entity_id')

    def __str__(self):
        return "{} #{}".format(
            self.entity_type.model_class().__name__,
            self.entity_id,
        )

    @property
    def expired(self):
        return (timezone.now() - self.timestamp) > timedelta(hours=24)

    @property
    def url(self):
        if self.entity_type == ContentType.objects\
                .get(app_label='links', model='link'):
            return self.entity.url

        if self.entity_type == ContentType.objects\
                .get(app_label='links', model='file'):
            return '{}{}'.format(settings.MEDIA_URL, self.entity.content)


class File(models.Model):
    """File model."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.FileField(upload_to='resources/')
    created_at = models.DateTimeField(auto_now=True)
    references = GenericRelation(Reference, related_query_name='file')


class Link(models.Model):
    """Link model."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now=True)
    references = GenericRelation(Reference, related_query_name='link')


class Redirect(models.Model):
    """Redirect model."""
    reference = models.ForeignKey(
        Reference,
        related_name='redirects',
        on_delete=models.CASCADE,
    )
    datestamp = models.DateField(auto_now=True)


class UserAgent(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    agent = models.CharField(max_length=255)
