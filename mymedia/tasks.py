# coding: utf-8
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from . import models
from mytaggit.utils import Kakasi
import os
import re


@receiver(pre_save, sender=models.MediaFile)
def on_mediafile_saving(sender, instance=None, **kwargs):
    if instance:
        name, ext = os.path.splitext(instance.data.name)
        instance.title = instance.title or os.path.basename(name)
        if not instance.filename:
            instance.filename = Kakasi().convert(instance.title).replace(' ', '-') + ext
            instance.filename = re.sub(r'--+', '-', instance.filename)
        instance.media_type = models.MediaType.objects.get_for(
            instance.data.name)


@receiver(post_save, sender=models.MediaFile)
def on_mediafile_saved(sender, instance=None, **kwargs):
    instance and instance.update_meta()
