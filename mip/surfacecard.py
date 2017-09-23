#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Split surface card into name, transform, type and list of coeffs.
"""

import re
import cards
import cardcontent

re_surface = re.compile(r"""^\s*([+*]*\d+)\s+
                            ([-+]*\d*\s*)
                            ([a-zA-Z/]+)\s+
                            (.*)$""", re.VERBOSE)


def split(txt):
    m = re_surface.search(txt)
    return m.groups()


def get_cards_from_file(fname):
    for c, n, t in cards.get_cards_from_file(fname,
                                             preservecommentlines=False,
                                             blocks='s'):
        c = cardcontent.card_content(c)
        yield n, split(c)


if __name__ == '__main__':
    from sys import argv
    for n, cc in get_cards_from_file(argv[1]):
        print n, cc
