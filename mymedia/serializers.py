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


    def update(self, instance, validated_data):
        new_filename = validated_data.get('filename', instance.filename)
        new_access = validated_data.get('access', instance.access)
        renamed = instance.filename != new_filename or \
            instance.access != new_access
        result = super(MediaFileSerializer, self).update(instance, validated_data)
        if renamed:
            result.set_new_name(instance.filename)
        return result


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Album
        fields = '__all__'
        read_only_fields = ('owner', )


class AlbumFileSerializer(serializers.ModelSerializer):
    mediafile = MediaFileSerializer(many=False)

    class Meta:
        model = models.AlbumFile
        # fields = ['id', 'album', 'mediafile', 'order']
        fields = '__all__'

    def create(self, validated_data):
        mediafile = validated_data.pop('mediafile')
        mediafile['owner'] = validated_data.pop('owner', None)
        validated_data['mediafile'] = \
            models.MediaFile.objects.create(**mediafile)
        res = super(AlbumFileSerializer, self).create(validated_data)
        return res

    def update(self, instance, validated_data):
        result = super(AlbumFileSerializer, self).update(instance, validated_data)
        return result
