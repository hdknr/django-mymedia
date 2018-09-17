from django.urls import reverse
from django.conf import settings


class ProtectionMixin(object):

    def protected_url(self, name, **kwargs):
        views = getattr(settings, 'MYMEDIA_PROTCTED_VIEW', {})
        for access, view in views.items():
            if name and name.startswith(access):
                return reverse(view, kwargs={'name': name})
