# coding: utf-8
from django.contrib import admin
from . import models


@admin.register(models.MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'data', 'access', 'owner', 'media_type', ]


@admin.register(models.ImageMeta)
class ImageMetaAdmin(admin.ModelAdmin):
    list_display = ['id', 'width', 'height', 'info', ]
    raw_id_fields = ['image', ]


@admin.register(models.ThumbnailProfile)
class ThumbnailProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'width', 'height', 'info', ]


@admin.register(models.Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'data', ]
    raw_id_fields = ['image', ]
