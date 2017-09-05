# coding: utf-8
from django.core.urlresolvers import reverse
from django.conf import settings


class ProtectionMixin(object):

    def protected_url(self, name, headers=None,
                      response_headers=None, expire=None):
        views = getattr(settings, 'PROTCTED_MEDIA_VIEW', {})
        for access, view in views:
            if name and name.startswith(access):
                return reverse(view, kwargs={'name': name})
