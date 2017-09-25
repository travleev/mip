#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from codecs import open
import tatsu
from tatsu.ast import AST

from semantics import GeomSemantics
import cellcard

grammar = open('grammars/geom.ebnf', 'r').read()
parser = tatsu.compile(grammar)

# patterns to replace space denoting intersection with '*'
re_union = re.compile('\s*:\s*')
re_pareno = re.compile('\(\s*')
re_parenc = re.compile('\s*\)')
re_spaces = re.compile('\s+')


def normalize(geom):
    """
    Replace spaces denoting intersection with `*`.

    Also replace '#' denoting complement with '_' .
    """
    g = geom.strip()

    # remove spaces around ':' operator
    g = re_union.sub(':', g)
    # remove spaces after '(' and before ')'
    g = re_pareno.sub('(', g)
    g = re_parenc.sub(')', g)
    # replace one or more spaces with exactly one ' '.
    g = re_spaces.sub('*', g)
    g = g.replace('#', '_')
    return g


def get_ast(geom):
    if 'like' in geom.lower():
        return geom.split()[1]
    g = normalize(geom)
    ast = parser.parse(g, semantics=GeomSemantics())
    return ast

def get_cards_from_file(fname):
    for n, cc in cellcard.get_cards_from_file(fname):
        name, mat, geom, opts = cc
        ast = get_ast(geom)
        yileld n, (name, mat, geom, ast, opts)


if __name__ == '__main__':
    import pprint
    from sys import argv

    for n, cc in get_cards_from_file(argv[1]):
        name, mat, geom, ast, opts = cc

        print '*'*60
        print n, repr(geom)
        ast = get_ast(geom)
        pprint.pprint(ast, indent=2, width=10)
