#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from codecs import open
import tatsu
from tatsu.ast import AST
from semantics import GeomSemantics

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
    g = re_union.sub(':', g)
    g = re_pareno.sub('(', g)
    g = re_parenc.sub(')', g)
    g = re_spaces.sub('*', g)
    g = g.replace('#', '_')
    return g


if __name__ == '__main__':
    import pprint
    import json
    from sys import argv
    from cellcard import get_cards_from_file

    for n, cc in get_cards_from_file(argv[1]):
        name, mat, geom, opts = cc

        print '*'*60
        print n, repr(geom)
        if 'like' not in geom.lower():
            g = normalize(geom)
            print n, repr(g)
            ast = parser.parse(g, semantics=GeomSemantics())
            pprint.pprint(ast, indent=2, width=20)
            print ast.evaluate()
            if isinstance(ast, AST):
                print json.dumps(ast.asjson(), indent=4)

        else:
            pprint.pprint(geom)
