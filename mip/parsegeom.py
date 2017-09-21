#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

GRAMMAR = """

    start = expr $;

    expr =
        | expr ':' isect
        | isect;

    isect =
        | isect '*' operand
        | operand;

    operand =
        | '(' @:expr ')'
        | surface;

    surface = /[-+]{0,1}\d+/;


"""

# patterns to replace space denoting intersection with '*'
re_union = re.compile('\s*:\s*')
re_spaces = re.compile('\s+')
re_pareno = re.compile('\(\s*')
re_parenc = re.compile('\s*\)')

if __name__ == '__main__':
    import tatsu
    import pprint
    import json
    from sys import argv
    from cellcard import get_cards_from_file

    for n, cc in get_cards_from_file(argv[1]):
        name, mat, geom, opts = cc

        print '*'*60
        print n, repr(geom)
        if 'like' not in geom.lower():
            g = geom.strip()
            g = re_union.sub(':', g)
            g = re_pareno.sub('(', g)
            g = re_parenc.sub(')', g)
            g = re_spaces.sub('*', g)
            print n, repr(g)
            ast = tatsu.parse(GRAMMAR, g)
            pprint.pprint(ast, indent=2, width=20)

        else:
            pprint.pprint(geom)
