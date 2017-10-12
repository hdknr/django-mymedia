# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from ordered_model.models import OrderedModel
from .files import ModelFieldPath


class StaticFile(models.Model):
    basename = models.CharField(max_length=200)

    class Meta:
        abstract = True


image_filename_validator = RegexValidator(
    regex=r'^[a-z]+[a-z\d\-\.]+$',
    message=_('your-beautifull-photo-01.jpg'))           # TODO: better message


class UploadTo(ModelFieldPath):

    def create_name(self, instance, filename):
        self.access = instance.access
        return super(UploadTo, self).create_name(instance, filename)


class MediaType(models.Model):
    content_type = models.CharField(max_length=200, unique=True)
    label = models.CharField(
        max_length=50, null=True, blank=True, default=None)

    class Meta:
        abstract = True


class MediaFileBase(models.Model):
    title = models.CharField(
        max_length=200, null=True, blank=True)
    ''' File Title '''
    filename = models.CharField(
        max_length=200, null=True, blank=True,
        validators=[image_filename_validator])
    ''' Original name or changed after '''
    data = models.FileField(upload_to=UploadTo('data'))
    access = models.CharField(
        max_length=15, default='protected',
        choices=(('protected', _('Protected')), ('public', _('Public'))))

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        abstract = True


class MediaFile(MediaFileBase):
    owner = models.ForeignKey(User)
    media_type = models.ForeignKey(
        MediaType, null=True, blank=True, default=None)

    class Meta:
        abstract = True


class ImageMeta(models.Model):
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    info = models.TextField(null=True, default=None, blank=True)

    class Meta:
        abstract = True


class UploadThumbnailTo(ModelFieldPath):

    def create_name(self, instance, filename):
        self.access = instance.image.access
        return super(UploadThumbnailTo, self).create_name(instance, filename)


class ThumbnailProfile(OrderedModel):
    name = models.CharField(max_length=20, unique=True)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    info = models.TextField(default='{}')

    class Meta:
        abstract = True


class Thumbnail(models.Model):
    data = models.FileField(upload_to=UploadThumbnailTo('data'))

    class Meta:
        abstract = True
