# encoding: utf-8
from rest_framework import serializers
from taggit_serializer.serializers import (
    TaggitSerializer, TagListSerializerField)
from . import models


class MediaTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MediaType
        fields = '__all__'


class MediaFileSerializer(TaggitSerializer, serializers.ModelSerializer):

    media_type = MediaTypeSerializer(many=False, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = models.MediaFile
        fields = '__all__'
        read_only_fields = ('owner', )

    def create(self, validated_data):
        data = validated_data.get('data', None)
        filename = validated_data.get('filename', None)
        if data and filename:
            data.name = filename
        return super(MediaFileSerializer, self).create(validated_data)
