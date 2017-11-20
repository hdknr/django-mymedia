from django.conf.urls import url, include
from . import views, api

urlpatterns = [
    url(r'^album', views.album_index, name="mymedia_album_index"),
    url(r'^filenames', views.filenames, name="filenames"),
    url(r'^api/', include(api)),
]
