# coding: utf-8
from django.conf import settings

# from storages.backends.s3boto import S3BotoStorage
from storages.backends.s3boto3 import S3Boto3Storage
from . import ProtectionMixin


class StaticStorage(S3Boto3Storage):
    location = getattr(settings, 'STATICFILES_LOCATION', '')


class MediaStorage(S3Boto3Storage, ProtecteionMixin):
    location = getattr(settings, 'MEDIAFILES_LOCATION', '')

    def url(self, name, headers=None, response_headers=None, expire=None):
        return self.protected_url(name) or super(MediaStorage, self).url(
            name, headers=headers, response_headers=response_headers,
            expire=expire)

    def get_available_name(self, name, max_length=None):
        ow = getattr(settings, 'MYMEDIA_OVERWRITE', '')

        if self.exists(name):
            if ow == 'delete':
                self.delete(name)
            elif ow == 'backup':
                self.move(name, name + ".bak")

        return super(MediaStorage, self).get_available_name(
            name, max_length=max_length

    def move(self, src_name, to_name):
        # TODO:
        # Create a new S# Bucket object, copy from original one and delete it.
        #
        src = self._encode_name(src_name)
        to = self._encode_name(to_name)
        self.bucket.Object(to).copy_from(src)
        self.delete(src_name)
