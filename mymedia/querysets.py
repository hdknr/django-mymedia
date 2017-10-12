# coding: utf-8
from django.db import models
from mimetypes import guess_type
from PIL import Image, ExifTags
from mptt.models import TreeManager
from . import encoders
import os


class PathManager(TreeManager):

    def from_path(self, full_path):
        paths = [i for i in full_path.split('/') if i]
        level = len(paths) - 1
        path = None
        for i in range(len(paths)):
            path, created = self.get_or_create(
                node=paths[i], level=i, parent=path)
        return path

class StaticFileQuerySet(models.QuerySet):

    def get_or_create_from_path(self, full_path):
        from . models import Path
        dirname = os.path.dirname(full_path)
        basename = os.path.basename(full_path)
        path = dirname and Path.objects.from_path(dirname)
        return self.get_or_create(path=path, basename=basename)


class MediaTypeQuerySet(models.QuerySet):

    def get_for(self, name):
        content_type, _x = guess_type(name)
        return content_type and \
            self.get_or_create(content_type=content_type)[0]


class MediaFileQuerySet(models.QuerySet):

    def filter_image(self, **kwargs):
        return self.filter(
            media_type__content_type__startswith='image/', **kwargs)


class ImageMetaQuerySet(models.QuerySet):

    def get_for(self, media):
        if media.media_type and \
                media.media_type.content_type.startswith('image'):
            img = Image.open(media.data)
            width, height = img.size
            try:
                exif = {
                        ExifTags.TAGS[k]: v
                        for k, v in img._getexif().items()
                        if k in ExifTags.TAGS
                }
            except:
                exif = {}

            info = {'dpi': img.info.get('dpi', None), 'exif': exif}
            try:
                info = encoders.BaseObjectEncoder.to_json(info, indent=2)
            except:
                info = '{}'

            medias = self.filter(image=media)
            if medias.update(width=width, height=height, info=info):
                return medias.first()
            else:
                return self.create(
                    image=media, width=width, height=height, info=info)
