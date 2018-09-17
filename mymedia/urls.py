from django.urls import re_path
from .views import download


urlpatterns = [
    re_path('^(?P<name>.+)',  download, name="mymedia-download"),
]
