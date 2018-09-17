from django.core.files.storage import FileSystemStorage
from django.core.files.move import file_move_safe
from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage as BaseStorage
from . import ProtectionMixin


class MediaStorage(FileSystemStorage, ProtectionMixin):

    def url(self, name):
        return self.protected_url(name) or super(MediaStorage, self).url(name)

    def get_available_name(self, name, max_length=None):
        ow = getattr(settings, 'MYMEDIA_OVERWRITE', '')

        if self.exists(name):
            if ow == 'delete':
                self.delete(name)
            elif ow == 'backup':
                self.move(name, name + ".bak")

        return super(MediaStorage, self).get_available_name(
            name, max_length=max_length)

    def move(self, src_name, to_name):
        file_move_safe(self.path(src_name), self.path(to_name))


class StaticStorage(BaseStorage):

    def get_available_name(self, name, max_length=None):
        ow = getattr(settings, 'MYMEDIA_OVERWRITE', 'delete')

        if self.exists(name):
            if ow == 'delete':
                self.delete(name)

        return super(StaticStorage, self).get_available_name(
            name, max_length=max_length)

    def move(self, src_name, to_name):
        file_move_safe(self.path(src_name), self.path(to_name))
