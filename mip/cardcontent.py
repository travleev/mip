#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

re_comment = re.compile('[$&].*$', re.MULTILINE)
re_spaces = re.compile('\s+')

"""
Extract content of cards (remove comments).
"""


def card_content(lines):
    """
    From a list of lines representing a card with comments, extract only
    meaningfull part (i.e. remove all comments and extra-spaces). The result is
    a one-line string.

    It is assumed that 1-st and last lines in the list are not comment lines
    (i.e.  that this text is obtained from cards.get_cards(False) generator.
    """

    # Remove in-line comments denoted by $ or &
    res = []
    for l in lines:
        res.extend(re_comment.split(l))

    # Remove multiple spaces
    res = ' '.join(res)
    res = re_spaces.sub(' ', res)
    return res


if __name__ == '__main__':
    from sys import argv
    from cards import get_cards_from_file
    import utils
    for c, n, t in get_cards_from_file(argv[1], preservecommentlines=False):
        c_orig = '\n'.join(c)
        c_cont = card_content(c)
        print n, t
        print repr(utils.shorten(c_orig))
        print repr(utils.shorten(c_cont))
