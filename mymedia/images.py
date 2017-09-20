# coding: utf-8
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def resize_image(image_field, image_format, width, height):
    img = Image.open(image_field)
    if img.size[0] > width or img.size[1] > height:
        new_img = img.resize((width, height))

    buf = BytesIO()
    new_img.save(fp=buf, format=image_format)
    return ContentFile(buf.getvalue())
