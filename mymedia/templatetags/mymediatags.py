# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from mymedia import forms, models
register = template.Library()


@register.simple_tag(takes_context=False)
def mediafile_form():
    return forms.MediaFileForm()


@register.filter
def thumbnail_url(media, profile='default'):
    tp = models.ThumbnailProfile.objects.filter(name=profile).first()
    tp_media = tp and tp.get_thumbnail_for(media)
    return tp_media and tp_media.data.url
