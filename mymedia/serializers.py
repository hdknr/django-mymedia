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


class OpenMediaFileSerializer(serializers.ModelSerializer):

    thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = models.MediaFile
        fields = ['id', 'title', 'data', 'thumbnails']

    def get_thumbnails(self, obj):
        request = self.context.get('request', None)

        def _url(path):
            return request and request.build_absolute_uri(path) or path

        return dict((i.profile.name, _url(i.data.url))
                    for i in obj.thumbnail_set.all())


class LocalMediaFileSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField()

    class Meta:
        model = models.MediaFile
        fields = ['id', 'data', ]
        read_only_fields = ['data']

    def get_data(self, obj):
        request = self.context.get('request', None)
        def _url(path):
            return request and request.build_absolute_uri(path) or path
        return _url(obj.data.url)


class AlbumSerializer(serializers.ModelSerializer):

    mediafiles = serializers.JSONField(write_only=True)

    class Meta:
        model = models.Album
        fields = ['id', 'title', 'owner', 'mediafiles', ]
        read_only_fields = ('owner', )

    def to_representation(self, obj):
        res = super(AlbumSerializer, self).to_representation(obj)
        res['mediafiles'] = [
            LocalMediaFileSerializer(i.mediafile, context=self.context).data
            for i in obj.albumfile_set.all()]
        return res

    def update(self, instance, validated_data):
        mediafiles = validated_data.pop('mediafiles', [])
        result = super(AlbumSerializer, self).update(instance, validated_data)
        print(mediafiles, validated_data)
        instance.update_files([i['id'] for i in mediafiles])
        return result


class AlbumFileSerializer(serializers.ModelSerializer):
    mediafile = MediaFileSerializer(many=False)
    new_order = serializers.IntegerField(required=False)

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
        mediafile = validated_data.pop('mediafile', None)
        ser = mediafile and MediaFileSerializer(
            instance.mediafile, data=mediafile, context=self.context)
        ser and ser.is_valid() and ser.save()
        result = super(AlbumFileSerializer, self).update(instance, validated_data)
        new_order = validated_data.get('new_order', None)
        if new_order:
            instance.to(new_order)
        return result
