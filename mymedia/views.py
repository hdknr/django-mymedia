from django.http import HttpResponse, HttpResponseForbidden
from .files import ModelFieldPath
from .utils import download_permcode
from mimetypes import guess_type


def download(request, name):
    '''download (protected) file '''
    instance, field = ModelFieldPath.get_protected_data(name)
    value = instance and getattr(instance, field, None)

    if not instance or not value or not hasattr(instance, 'has_perm'):
        return HttpResponseForbidden()

    is_valid = instance.has_perm(
        request.user, download_permcode(instance, field), request=request)

    if not is_valid:
        return HttpResponseForbidden()

    ct, _x = guess_type(name)
    return HttpResponse(value, content_type=ct)