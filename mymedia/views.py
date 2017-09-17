# coding: utf-8
from django.http import HttpResponse, HttpResponseForbidden
from mymedia.files import ModelFieldPath
from mimetypes import guess_type


def download(request, name):
    '''download (protected) file '''
    value = ModelFieldPath.get_protected_data(name, request.user, 'download')
    if not value:
        return HttpResponseForbidden()

    ct, _x = guess_type(name)
    return HttpResponse(value, content_type=ct)
