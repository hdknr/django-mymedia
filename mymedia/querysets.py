# coding: utf-8
from django.db import models
from mimetypes import guess_type
from PIL import Image, ExifTags
from . import encoders


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
