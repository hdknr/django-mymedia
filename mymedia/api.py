# coding: utf-8
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'openmediafiles', viewsets.OpenMediaFileViewSet, base_name='open/mediafile')
router.register(r'mediafiles', viewsets.MediaFileViewSet, base_name='mediafile')
router.register(r'thumbnails', viewsets.ThumbnailViewSet, base_name='thumbnail')
router.register(r'imagefiles', viewsets.ImageFileViewSet, base_name='imagefile')
router.register(r'albums', viewsets.AlbumViewSet, base_name='album')
router.register(r'albumfiles', viewsets.AlbumFileViewSet, base_name='albumfile')

urlpatterns = [
    url(r'^rest/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]
