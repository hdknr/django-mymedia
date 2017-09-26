# coding: utf-8
from mytaggit.utils import Kakasi


def slugify(name):
    return Kakasi().convert(name)
