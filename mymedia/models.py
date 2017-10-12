# coding: utf-8

from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from mytaggit.models import TaggableManager
from . import querysets, defs, methods


class Path(MPTTModel):
    node = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        unique_together = (('node', 'parent'), )

    class MPTTMeta:
        order_insertion_by = ['node']

    objects = querysets.PathManager()

    def __str__(self):
        return self.node

    @property
    def full_path(self):
        return '/'.join(i.node for i in self.get_ancestors(include_self=True))


class StaticFile(defs.StaticFile, methods.StaticFile):
    path = models.ForeignKey(Path, null=True, default=None, blank=True)

    class Meta:
        unique_together = (('path', 'basename'), )

    objects = querysets.StaticFileQuerySet.as_manager()


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
        ordering = ['-id', ]

    def __str__(self):
        return self.filename

    objects = querysets.MediaFileQuerySet.as_manager()
    tags = TaggableManager()


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
        ordering = ['order', ]

    def __str__(self):
        return "{}({} x {})".format(self.name, self.width, self.height)


class Thumbnail(defs.Thumbnail):
    image = models.ForeignKey(MediaFile)
    profile = models.ForeignKey(ThumbnailProfile)

    class Meta:
        verbose_name = _('Thumbnail')
        verbose_name_plural = _('Thumbnails')
