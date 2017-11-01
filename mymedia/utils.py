# coding: utf-8
from django.template.loader import get_template
from django.template.library import SimpleNode
from django.template.loader_tags import BlockNode, ExtendsNode
from mytaggit.utils import Kakasi


def slugify(name):
    return Kakasi().convert(name)


def find_tags(template_name, node_name):
    def _finds(nodes):
        for n in nodes:
            if isinstance(n, SimpleNode) and n.token:
                tokens = n.token.split_contents()
                if tokens[0] == node_name:
                    yield (tokens, n)
            elif isinstance(n, ExtendsNode) and \
                    isinstance(n.parent_name.var, str):
                yield from _finds(get_template(n.parent_name.var).template)
            else:
                for i in n.child_nodelists:
                    yield from _finds(getattr(n, i, []))

    return _finds(get_template(template_name).template)


def find_blocks(template_name):
    def _finds(nodes):
        for n in nodes:
            if isinstance(n, BlockNode):
                yield n
            elif isinstance(n, ExtendsNode) and \
                    isinstance(n.parent_name.var, str):
                yield from _finds(get_template(n.parent_name.var).template)
            else:
                for i in n.child_nodelists:
                    yield from _finds(getattr(n, i, []))

    return _finds(get_template(template_name).template)
