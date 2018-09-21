'''
from django.urls import re_path
from mymedia.views import download
from varidators import check_perm

urlpatterns = [
    re_path(r'^media/(?P<name>.+)$',  download, {'validator': check_perm}),
    ....
]
'''

from django.http import HttpResponse, HttpResponseForbidden
from .files import ModelFieldPath
from mimetypes import guess_type


def download(request, name, validator=None):
    '''download (protected) file '''
    instance, field = ModelFieldPath.get_protected_data(name)
    is_valid = validator(request, instance, field) if validator else True
    value = getattr(instance, field, None)
    # CHECK
    if not instance or not is_valid or not value:
        return HttpResponseForbidden()
    ct, _x = guess_type(name)
    return HttpResponse(value, content_type=ct)