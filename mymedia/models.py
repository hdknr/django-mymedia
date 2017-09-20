# coding: utf-8

from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from . import querysets, defs, methods


class MediaType(defs.MediaType):

    class Meta:
        verbose_name = _('Media Type')
        verbose_name_plural = _('Media Types')

    objects = querysets.MediaTypeQuerySet.as_manager()

    def __str__(self):
        return self.label or self.content_type


class MediaFile(defs.MediaFile, methods.MediaFile):

    class Meta:
        verbose_name = _('Media File')
        verbose_name_plural = _('Media Files')

    def __str__(self):
        return self.filename

    objects = querysets.MediaFileQuerySet.as_manager()


class ImageMeta(defs.ImageMeta):
    image = models.OneToOneField(MediaFile)

    class Meta:
        verbose_name = _('Image Meta')
        verbose_name_plural = _('Image Meta')

    objects = querysets.ImageMetaQuerySet.as_manager()


class ThumbnailProfile(
    defs.ThumbnailProfile, methods.ThumbnailProfile,
):

    class Meta:
        verbose_name = _('Thumbnail Profile')
        verbose_name_plural = _('Thumbnail Profiles')

    def __str__(self):
        return self.name


class Thumbnail(defs.Thumbnail):
    image = models.ForeignKey(MediaFile)
    profile = models.ForeignKey(ThumbnailProfile)

    class Meta:
        verbose_name = _('Thumbnail')
        verbose_name_plural = _('Thumbnails')
