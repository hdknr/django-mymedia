# coding: utf-8
from django.utils.deconstruct import deconstructible
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_permission_codename
from django.utils.six.moves.urllib.parse import unquote
from django.utils.timezone import now
import traceback
import re
import os
from .utils import slugify

from logging import getLogger
logger = getLogger()


@deconstructible
class ModelFieldPath(object):
    '''
    photo = models.ImageField(upload_to=MediaFieldPath('photo')..)
    '''

    def __init__(self, fieldname, access='protected'):
        self.fieldname = fieldname or 'file'
        self.access = access

    def __call__(self, instance, filename):
        try:
            name = slugify(self.create_name(instance, filename))
            res = self.get_filepath(
                self.access, instance._meta.app_label,
                instance._meta.model_name, self.fieldname, name)
            return res
        except:
            logger.error(traceback.format_exc())

    def create_name(self, instance, filename):
        n = now()
        id = instance.id or "t{:x}".format(int(n.strftime('%H%M%S')))
        prefix = n.strftime("%Y/%m%d")
        return u"{}/{}.{}".format(prefix, id, filename)

    @classmethod
    def get_base_url(cls, access, app_label, model_name, field_name):
        return u'{}/{}/{}/{}'.format(
            access, app_label, model_name, field_name)

    @classmethod
    def get_filepath(cls, access, app_label, model_name, field_name, name):
        ret = u'{}/{}'.format(
            cls.get_base_url(access, app_label, model_name, field_name), name)
        return unquote(ret)

    @classmethod
    def get_protected_data(cls, name, user, action='download'):
        m = re.search(
            r'^(?P<access>[^/]+)/(?P<app_label>[^/]+)/(?P<model_name>[^/]+)/(?P<field_name>[^/]+)/(?P<path>.+)',    # NOQA
            name)
        access, app_label, model_name, field_name, path = m and m.groups() or tuple([None] * 5)    # NOQA
        ct = ContentType.objects.get(
            app_label=app_label, model=model_name)
        model_class = ct and ct.model_class()
        query = Q(**{field_name: path}) | Q(**{field_name: name})
        instance = model_class.objects.filter(query).first()
        perm = get_permission_codename(action, model_class._meta)
        # TODO: cache for S3 storage
        return user.has_perm(perm, instance) and getattr(instance, field_name)
