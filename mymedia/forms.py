# coding: utf-8
from django import forms
from . import models


class MediaFileForm(forms.ModelForm):

    class Meta:
        model = models.MediaFile
        exclude = ['owner', 'media_type', ]


class StaticFileForm(forms.ModelForm):
    data = forms.FileField(required=False)
    new_path = forms.CharField(required=False)

    class Meta:
        model = models.StaticFile
        exclude = ['basename', 'path']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)
        if instance:
            initial['new_path'] = instance.full_path
        kwargs['initial'] = initial
        super(StaticFileForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        new_path = self.cleaned_data.get('new_path', None)
        old = self.instance.full_path
        if new_path:
            spec = models.StaticFile.objects.path_and_basename(new_path)
            self.instance.path = spec['path']
            self.instance.basename = spec['basename']
        if old != self.instance.full_path:
            # TODO: move
            pass

        res = super(StaticFileForm, self).save(*args, **kwargs)

        data = self.cleaned_data.get('data', None)
        data and res.update_content(data)

        return res
