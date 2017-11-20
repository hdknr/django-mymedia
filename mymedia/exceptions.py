# coding: utf-8
'''
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'mymedia.exceptions.exception_handler'
}
'''
from rest_framework.views import exception_handler as default_handler
from rest_framework.response import Response
from rest_framework import status
from .encoders import BaseObjectEncoder
import traceback


def exception_handler(exc, context):
    print(traceback.format_exc())
    response = default_handler(exc, context)
    setattr(exc, 'exc', exc.__class__.__name__)
    content = BaseObjectEncoder.to_json(exc)
    return Response(content, status=status.HTTP_400_BAD_REQUEST)
