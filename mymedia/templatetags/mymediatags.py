# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from django.middleware.csrf import get_token

from mymedia import forms, models
register = template.Library()


@register.simple_tag(takes_context=False)
def mediafile_form():
    return forms.MediaFileForm()


@register.filter
def thumbnail_url(media, profile='default'):
    t = media.thumbnail_for(profile)
    return t and t.data.url


@register.simple_tag(takes_context=True)
def get_csrftoken(context):
    request = context.get('request', None)
    token = request and get_token(request)
    return token
