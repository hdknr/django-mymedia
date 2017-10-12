# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.files import File
import djclick as click
from ... import models
from logging import getLogger
logger = getLogger()


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.argument('path')
@click.argument('user_id')
@click.option('--public', '-p', is_flag=True)
@click.pass_context
def add_mediafile(ctx, path, user_id, public):
    ''' Add a MediaFile'''
    access = 'public' if public else 'protected'
    models.MediaFile(
        data=File(open(path, 'rb')),
        access=access,
        owner=User.objects.filter(id=user_id).first()
    ).save()


@main.command()
@click.argument('src')
@click.argument('dst')
@click.pass_context
def add_staticfile(ctx, src, dst):
    '''Add a static file'''
    data = File(open(src, 'rb'))
    staticfile, _x = models.StaticFile.objects.get_or_create_from_path(dst)
    staticfile and staticfile.update_content(data)
