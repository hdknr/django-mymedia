from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.base import ContentFile


def image_info(image_field):
    img = Image.open(image_field)
    return pil_image_info(img)


def resize(image_field, width, height, image_format=None):
    buf = BytesIO()
    original =Image.open(image_field)
    if img.size[0] > width or img.size[1] > height:
        new_img = img.resize((width, height))
        new_img.save(fp=buf, format=image_format or original.format)
    else:
        img.save(fp=buf, format=image_format or original.format)

    return ContentFile(buf.getvalue())


def fit(image_field, width, height, background=None, image_format=None):
    buf = BytesIO()
    original = Image.open(image_field)
    img = pil_fit(original, width, height)
    img.save(fp=buf, format=image_format or original.format)
    return ContentFile(buf.getvalue())


def crop_rect(image_field, crop_width, crop_height, image_format=None):
    buf = BytesIO()
    original = Image.open(image_field)
    img = pil_crop_center(original, crop_width, crop_height)
    img.save(fp=buf, format=image_format or original.format)
    return ContentFile(buf.getvalue())


def fit_and_crop_rect(
        image_field, crop_width, crop_height, background=None, image_format=None):
    buf = BytesIO()
    original =Image.open(image_field)
    img = pil_crop_rect(
        pil_fit(original, crop_width, crop_height),
        crop_width, crop_height, background=background)
    img.save(fp=buf, format=image_format or original.format)
    return ContentFile(buf.getvalue())


def pil_fit(pil_img, width, height):
    copied = pil_img.copy()
    length = max(width, height)
    copied.thumbnail((length, length), Image.LANCZOS)
    return copied


def pil_image_info(pil_img):
    width, height = img.size
    try:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
    except:
        exif = {}
    info = {'width': width, 'height': height,
            'dpi': img.info.get('dpi', None), 'exif': exif}
    return info


def make_crop_rect(original, crop):
    '''(width, height), (width, height)'''
    x = (original[0] - crop[0]) // 2
    y = (original[1] - crop[1]) // 2
    width = (original[0] + crop[0]) // 2
    height = (original[1] + crop[1]) // 2
    return (x, y, width, height)


def pil_fill_background(pil_img, width, height, background):
    if pil_img.width < width and pil_img.height <= height:
        return pil_image

    to_rect = (min(pil_img.width, width), min(pil_img.height, height))
    new = pil_img.crop(make_crop_rect(pil_img.size, to_rect))

    result = Image.new(pil_img.mode, pil_img.size, background)
    result.paste(new, ((result.width - new.width) // 2,
                       (result.height - new.height) // 2))
    return result


def pil_crop_rect(pil_img, crop_width, crop_height, background=None):
    ''' pil_img : PIL.Image'''
    new = pil_img.crop(make_crop_rect(pil_img.size, (crop_width, crop_height)))
    if background:
        return pil_fill_background(
            new, pil_img.width, pil_img.height, background)
    return new
