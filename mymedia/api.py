# coding: utf-8
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mediafiles', views.MediaFileViewSet, base_name='mediafile')
router.register(r'imagefiles', views.ImageFileViewSet, base_name='imagefile')
router.register(r'albums', views.AlbumViewSet, base_name='album')
router.register(r'albumfiles', views.AlbumFileViewSet, base_name='albumfile')

urlpatterns = [
    url(r'^api/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^filenames', views.filenames, name="filenames"),
    url(r'^', include(router.urls)),
]
