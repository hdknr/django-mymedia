# coding: utf-8
from django.contrib import admin
from django.utils.safestring import SafeString as _S
from ordered_model.admin import OrderedModelAdmin
from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField
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
    list_display = ['id', 'order', 'name', 'width', 'height', 'info', 'move_up_down_links', ]


@admin.register(models.Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'data', ]
    raw_id_fields = ['image', ]


@admin.register(models.Path)
class PathAdmin(MPTTModelAdmin):
    pass


@admin.register(models.StaticFile)
class StaticFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_path', 'basename', ]
    readonly_fields = ['full_path', 'link', ]

    def link(self, obj):
        return _S('<a href="{u}">{u}</a>'.format(u=obj.url))
