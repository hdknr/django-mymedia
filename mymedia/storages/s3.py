# coding: utf-8
from django.conf import settings

from storages.backends.s3boto import S3BotoStorage
from . import ProtectionMixin


class StaticStorage(S3BotoStorage):
    location = getattr(settings, 'STATICFILES_LOCATION', '')


class MediaStorage(S3BotoStorage, ProtecteionMixin):
    location = getattr(settings, 'MEDIAFILES_LOCATION', '')

    def url(self, name, headers=None, response_headers=None, expire=None):
        return self.protected_url(name) or super(MediaStorage, self).url(
            name, headers=headers, response_headers=response_headers,
            expire=expire)
