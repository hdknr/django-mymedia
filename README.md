# django-mymedia

- Bootstrap4 and bootstrap-vue
- protected media file management


## Protected Media

- If `name` starts with `protected',  the data is published through `download` view.
- `download` view finds the model instance for the given name, and publishes it
   if requesing user has  `download` permission for this instance.

settings.py:

~~~py
from django.conf import global_settings
...
AUTHENTICATION_BACKENDS = [
    'mymedia.backends.PermissionBackend',
] + global_settings.AUTHENTICATION_BACKENDS
DEFAULT_FILE_STORAGE = 'mymedia.storages.locals.MediaStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MYMEDIA_PROTCTED_VIEW = {'protected': 'private_media', }
~~~

urls.py:

~~~py
...
from mymedia.views import download
urlpatterns = [
    ...
    url(r'^private/(?P<name>.+)', download, name="private_media"),
    ...
]
~~~

models.py:

~~~py
# coding: utf-8
from django.db import models
from mymedia.files import ModelFieldPath
import re

class Document(models.Model):
    ...
    secret = models.FileField(
        upload_to=ModelFieldPath('secret', 'protected'),
        null=True, blank=True, default=None)

    def permcode_items(self, perm_code):
        p = re.split(r"[._]", perm_code) + [None, None, None]
        return dict(zip(['app_label', 'action', 'model'], p[:3]))

    def has_perm(self, user, permcode):
        pm = self.permcode_items(permcode)
        if user.is_authenticated() and pm['action'] == 'download':
            return True
        return False        
~~~
