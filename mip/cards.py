#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

"""
Split one block of MCNP input file into separate cards and inter-card comments.

Definition: C-comment is a comment line inside a card. B-comment is a comment
line between cards, i.e. above the line where the next card begins. Several
lines with B-comments compose a multi-line B-comment.

Two types of elements in the resulting list: cards and B-comments. Both are,
generally, multi-line strings.

Card is a part of the block containing all lines belonging to a card, together
with comments inside the card.

"""


def get_cards(block):
    """

    """
    for l in block.splitlines():
        if is_comment_line(l):
            print repr(l)


def is_comment_line(l):
    """
    Checks that l is a comment line.

    Comment line is a line whose 1-st non-white character is "c" or "C"
    followed by end-of-line of a space. The character "c" or "C" must
    be within first 5 characters of the line.
    """
    r = re.compile('^\s{0,4}[cC][ \r\n]')
    return bool(r.match(l))


if __name__ == '__main__':
    from sys import argv
    from blocks import get_block_positions
    text = open(argv[1]).read()

    dbi = get_block_positions(text)

    get_cards(text[slice(*dbi['c'])])
