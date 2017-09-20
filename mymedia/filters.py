# coding: utf-8
import rest_framework_filters as filters
from . import models


class MediaFileFilter(filters.FilterSet):

    class Meta:
        model = models.MediaFile
        fields = {
            'filename':  ['contains', 'exact', 'in', 'startswith'],
            'media_type__content_type': ['startswith'],
        }
