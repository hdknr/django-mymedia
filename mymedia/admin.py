# coding: utf-8
from django.contrib import admin
from . import models


@admin.register(models.MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'data', 'access', 'owner', ]
