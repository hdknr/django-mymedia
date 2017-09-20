# coding: utf-8
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, pagination
from mymedia.files import ModelFieldPath
from mimetypes import guess_type
from . import models, serializers, filters


def download(request, name):
    '''download (protected) file '''
    value = ModelFieldPath.get_protected_data(name, request.user, 'download')
    if not value:
        return HttpResponseForbidden()

    ct, _x = guess_type(name)
    return HttpResponse(value, content_type=ct)


class Pagination(pagination.PageNumberPagination):
    page_size = 16
    max_page_size = 16
    page_size_query_param = 'page_size'


class MediaFileViewSet(viewsets.ModelViewSet):

    queryset = models.MediaFile.objects.all()
    serializer_class = serializers.MediaFileSerializer
    filter_class = filters.MediaFileFilter
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination

    def get_queryset(self):
        return self.request.user.mediafile_set.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageFileViewSet(MediaFileViewSet):

    def get_queryset(self):
        return self.request.user.mediafile_set.filter_image()
