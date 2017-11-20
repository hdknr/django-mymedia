from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mymedia.files import ModelFieldPath
from mimetypes import guess_type
from . import utils
import os


def download(request, name):
    '''download (protected) file '''
    value = ModelFieldPath.get_protected_data(name, request.user, 'download')
    if not value:
        return HttpResponseForbidden()

    ct, _x = guess_type(name)
    return HttpResponse(value, content_type=ct)


@api_view(['POST'])
def filenames(request):
    name = request.POST.get('filename', '')
    name = os.path.basename(name)
    res = {'title': name, 'filename': utils.slugify(name)}
    return Response(res)


@staff_member_required
def album_index(request):
    '''request.user's Album list'''
    return TemplateResponse(
        request, 'mymedia/album/index.html', {})
