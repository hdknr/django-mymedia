from collections import OrderedDict
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, pagination
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
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination

    def get_queryset(self):
        return self.request.user.mediafile_set.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageFileViewSet(MediaFileViewSet):

    def get_queryset(self):
        return self.request.user.mediafile_set.filter_image()


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    filter_class = filters.AlbumFilter
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination

    def get_queryset(self):
        return self.request.user.album_set.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AlbumFileViewSet(viewsets.ModelViewSet):
    queryset = models.AlbumFile.objects.all()
    serializer_class = serializers.AlbumFileSerializer
    filter_class = filters.AlbumFileFilter
    permission_classes = (IsAuthenticated, )
    pagination_class = Pagination

    def get_queryset(self):
        res = super(AlbumFileViewSet, self).get_queryset()
        return res.filter(album__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
