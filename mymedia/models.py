# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .files import ModelFieldPath


class UploadTo(ModelFieldPath):

    def create_name(self, instance, filename):
        self.access = instance.access
        return super(UploadTo, self).create_name(instance, filename)


class MediaFile(models.Model):
    owner = models.ForeignKey(User)
    filename = models.CharField(
        max_length=200, null=True, blank=True)
    ''' Original name or changed after '''
    data = models.FileField(upload_to=UploadTo('data'))
    access = models.CharField(
        max_length=15, default='protected',
        choices=(('protected', _('Protected')), ('public', _('Public'))))

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Media File')
        verbose_name_plural = _('Media Files')

    def save(self, *args, **kwargs):
        self.filename = self.filename or self.data.name
        super(MediaFile, self).save(*args, **kwargs)

    def move_to(self, name):
        self.data.storage.move(self.data.name, name)
        self.data.name = name
        self.save()
