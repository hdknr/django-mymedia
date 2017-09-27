# coding: utf-8
from django import forms
from . import models


class MediaFileForm(forms.ModelForm):

    class Meta:
        model = models.MediaFile
        exclude = ['owner', 'media_type', ]
