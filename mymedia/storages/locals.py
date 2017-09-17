# coding: utf-8
from django.core.files.storage import FileSystemStorage
from . import ProtectionMixin


class MediaStorage(FileSystemStorage, ProtectionMixin):

    def url(self, name):
        return self.protected_url(name) or super(MediaStorage, self).url(name)
