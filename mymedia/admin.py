# coding: utf-8
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from . import models


class ThumbnailAdminInline(admin. TabularInline):
    model = models.Thumbnail


@admin.register(models.MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'data', 'access', 'owner', 'media_type', ]
    inlines = [ThumbnailAdminInline]


@admin.register(models.ImageMeta)
class ImageMetaAdmin(admin.ModelAdmin):
    list_display = ['id', 'width', 'height', 'info', ]
    raw_id_fields = ['image', ]


@admin.register(models.ThumbnailProfile)
class ThumbnailProfileAdmin(OrderedModelAdmin):
    list_display = ['id', 'order', 'width', 'height', 'info', 'move_up_down_links', ]


@admin.register(models.Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'data', ]
    raw_id_fields = ['image', ]
