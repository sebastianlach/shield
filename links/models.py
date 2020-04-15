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
        return "[{}:{}] {}".format(
            self.entity_type.model_class().__name__,
            self.entity_id,
            str(self.entity)
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
    content = models.FileField(upload_to='resources/')
    created_at = models.DateTimeField(auto_now=True)
    references = GenericRelation(Reference, related_query_name='file')

    def __str__(self):
        return "{} #{}".format(self.__class__.__name__, self.id)


class Link(models.Model):
    """Link model."""
    url = models.URLField()
    created_at = models.DateTimeField(auto_now=True)
    references = GenericRelation(Reference, related_query_name='link')

    def __str__(self):
        return "{} #{}".format(self.__class__.__name__, self.id)
