# encoding: utf-8
from rest_framework import serializers
from . import models


class MediaTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MediaType
        fields = '__all__'


class MediaFileSerializer(serializers.ModelSerializer):

    media_type = MediaTypeSerializer(many=False, read_only=True)

    class Meta:
        model = models.MediaFile
        fields = '__all__'
        read_only_fields = ('owner', )
