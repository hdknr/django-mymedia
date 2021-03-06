# coding: utf-8
from django.contrib.staticfiles.storage import staticfiles_storage
from . import images
from . import encoders
import os


class StaticFile(object):

    @property
    def full_path(self):
        return self.path and '/'.join([self.path.full_path, self.basename]) \
            or self.basename

    def update_content(self, fileobj):
        staticfiles_storage.save(self.full_path, fileobj)

    @property
    def url(self):
        return staticfiles_storage.url(self.full_path)


class MediaFile(object):

    def move_to(self, name):
        self.data.storage.move(self.data.name, name)
        self.data.name = name
        self.filename = os.path.basename(name)
        self.save()

    def build_new_filename(self, name):
        upload_to = self._meta.get_field('data').upload_to
        _x, ext = os.path.splitext(self.data.name)
        name =  name if name.endswith(ext) else name + ext
        return upload_to(self, name)

    def set_new_name(self, name):
        return self.move_to(self.build_new_filename(name))

    def update_meta(self):
        if self.media_type.content_type.startswith('image'):
            from . import models
            return models.ImageMeta.objects.get_for(self)


class ThumbnailProfile(object):

    def get_thumbnail_for(self, media):
        image_format = media.media_type.content_type.split('/')[1]
        resized = images.resize_image(
            media.data, image_format, self.width, self.height)
        resized.name = os.path.basename(media.data.name)

        thumbnail = media.thumbnail_set.filter(profile=self).first()
        if thumbnail:
            thumbnail.data = resized
            thumbnail.save()
        else:
            media.thumbnail_set.create(profile=self, data=resized)

        return thumbnail


class Album(object):
    def update_files(self, file_list):
        dels = set(i.id for i in self.files.all()) - set(file_list)
        self.albumfile_set.filter(mediafile_id__in=list(dels)).delete()
        for i in file_list:
            mf, created = self.albumfile_set.get_or_create(mediafile_id=i)
            mf.order = file_list.index(i) + 1
            print("update_files", i, mf.order)
            mf.save()

    @property
    def files_in_order(self):
        return [i.mediafile for i in self.albumfile_set.all()]

    @property
    def files_in_json(self):
        from .serializers import MediaFileSerializer
        return encoders.BaseObjectEncoder.to_json(
            MediaFileSerializer(self.files_in_order, many=True).data)
