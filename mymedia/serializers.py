# encoding: utf-8
from django.forms.models import model_to_dict
from django.db.models import Model
from django.db.models.fields.files import FieldFile
from datetime import datetime
from enum import Enum
from decimal import Decimal
import json


class BaseObjectEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, Model):
            return model_to_dict(obj)
        if isinstance(obj, FieldFile):
            return {'url': obj.url, 'name': obj.name}
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, object):
            ex = obj._excludes if hasattr(obj, '_excludes') else {}
            vals = obj._customes.copy() if hasattr(obj, '_customs') else {}
            vals.update(getattr(obj, '__dict__', {}))
            return dict([(k, v) for k, v in vals.items()
                         if k not in ex and not k.startswith('_') and v])
        return super(BaseObjectEncoder, self).default(obj)

    @classmethod
    def to_json(cls, obj, *args, **kwargs):
        return json.dumps(obj, cls=cls, *args, **kwargs)

    @classmethod
    def from_json(cls, jsonstr,  *args, **kwargs):
        return json.loads(jsonstr, *args, **kwargs)
