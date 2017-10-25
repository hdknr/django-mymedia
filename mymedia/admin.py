# coding: utf-8
from django.contrib import admin
from django.utils.safestring import SafeString as _S
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin
from ordered_model.admin import OrderedTabularInline
from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField
from . import models, forms


class ThumbnailAdminInline(admin. TabularInline):
    model = models.Thumbnail


@admin.register(models.MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if hasattr(obj, 'imagemeta'):
            return format_html('<img src="{}" width="100px"/>'.format(
                obj.data.url))
    image_tag.short_description = 'Image'

    list_display = ['id', 'image_tag', 'data', 'access', 'owner', 'media_type', ]
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
    form = forms.StaticFileForm
    list_display = ['id', 'full_path', 'basename', ]
    readonly_fields = ['full_path', 'link', ]

    def link(self, obj):
        return _S('<a href="{u}">{u}</a>'.format(u=obj.url))


class AlbumFileAdminInline(OrderedTabularInline):
    def image_tag(self, obj):
        if obj.mediafile and hasattr(obj.mediafile, 'imagemeta'):
            return format_html('<img src="{}" width="100px"/>'.format(
                obj.mediafile.data.url))
    image_tag.short_description = 'Image'

    model = models.AlbumFile
    extra = 1
    raw_id_fields = ['mediafile', ]
    readonly_fields = ['image_tag', 'order', 'move_up_down_links', ]


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumFileAdminInline, ]
    list_display = ['id', 'owner', 'title', ]
    raw_id_fields = ['owner', ]

    def get_urls(self):
        urls = super(AlbumAdmin, self).get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls
