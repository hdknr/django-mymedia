# coding: utf-8
from . import images
import os


class MediaFile(object):

    def move_to(self, name):
        self.data.storage.move(self.data.name, name)
        self.data.name = name
        self.save()

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
