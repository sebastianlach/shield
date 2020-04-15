from rest_framework import serializers

from .models import Link, File, Reference


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'name', 'created_at', 'updated_at')


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'created_at', 'updated_at')


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        timestamp = serializers.DateTimeField()
        files = serializers.CharField()
        fields = ('timestamp', 'entity')
