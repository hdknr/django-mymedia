from collections import OrderedDict
from rest_framework import viewsets, pagination, permissions
from rest_framework.response import Response
from . import models, serializers, filters


class Pagination(pagination.PageNumberPagination):
    page_size = 16
    max_page_size = 16
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_range', list(self.page.paginator.page_range)),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class MediaFileViewSet(viewsets.ModelViewSet):

    queryset = models.MediaFile.objects.all()
    serializer_class = serializers.MediaFileSerializer
    filter_class = filters.MediaFileFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = Pagination

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.MediaFile.objects.filter(access="public")
        return self.request.user.mediafile_set.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageFileViewSet(MediaFileViewSet):

    def get_queryset(self):
        return self.request.user.mediafile_set.filter_image()


class OpenMediaFileViewSet(viewsets.ModelViewSet):
    # TODO: IsAuthenticatedOrReadOnly to MediaFileViewSet
    queryset = models.MediaFile.objects.all()
    serializer_class = serializers.OpenMediaFileSerializer
    filter_class = filters.MediaFileFilter
    pagination_class = Pagination


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    filter_class = filters.AlbumFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    # Guest cant GET, HEAD or OPTIONS
    pagination_class = Pagination

    def get_queryset(self):
        # TODO: this method can be dropped.
        if self.request.user.is_authenticated():
            return self.request.user.album_set.all()
        return models.Album.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AlbumFileViewSet(viewsets.ModelViewSet):
    queryset = models.AlbumFile.objects.all()
    serializer_class = serializers.AlbumFileSerializer
    filter_class = filters.AlbumFileFilter
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = Pagination

    def get_queryset(self):
        res = super(AlbumFileViewSet, self).get_queryset()
        return res.filter(album__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        order = self.request.data.get('order', 0)   # TODO: POST
        params = order and {'order': order} or {}
        serializer.save(**params)


class ThumbnailViewSet(viewsets.ModelViewSet):

    queryset = models.Thumbnail.objects.all()
    serializer_class = serializers.ThumbnailSerializer
    filter_class = filters.ThumbnailFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
