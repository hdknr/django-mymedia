# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from mymedia import forms
register = template.Library()


@register.simple_tag(takes_context=False)
def mediafile_form():
    return forms.MediaFileForm()
