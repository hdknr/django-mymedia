# coding: utf-8
from django.db.models.signals import pre_save
from django.dispatch import receiver
from . import models


@receiver(pre_save, sender=models.MediaFile)
def on_medafile_saving(sender, instance=None, **kwargs):
    if instance:
        instance.filename = instance.filename or instance.data.name
        instance.media_type = models.MediaType.objects.get_for(
            instance.data.name)
