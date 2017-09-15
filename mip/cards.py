#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import utils

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

re_comment = re.compile('^\s{0,4}[cC](\s|$)')
re_continuation = re.compile('^\s{5,}')


def get_cards(block):
    """

    """

    cmnt = []
    card = []
    n_card = 0
    n_cmnt = 0
    # Function used at two places below
    def _yield():
        if card:
            yield card, n_card, 'card'
        if cmnt:
            yield cmnt, n_cmnt, 'cmnt'
    lprev = None  # previous card line
    for n, l in enumerate(block.splitlines()):
        # if comment, then  add to block of comments
        # if continuation, then append block of comment this line to current
        # card
        # if new card, then yield current card or current block of comments and
        # create a new current card
        if is_comment_line(l):
            cmnt.append(l)
        elif is_continuation(l, lprev):
            if cmnt:
                card.extend(cmnt)
                cmnt = []
                n_cmnt = n + 1
            card.append(l)
            lprev = l
        else:
            # this must be begin of a new card
            for r in _yield(): yield r
            cmnt = []
            n_cmnt = n + 1
            card = [l]
            n_card = n
            lprev = l
    # At the end of block, yield the last card and comments (this code must be
    # the same as in `else` clause above)
    for r in _yield(): yield r


def is_comment_line(l):
    """
    Checks that l is a comment line.

    Comment line is a line whose 1-st non-white character is "c" or "C"
    followed by end-of-line of a space. The character "c" or "C" must
    be within first 5 characters of the line.
    """
    return bool(re_comment.match(l))


def is_continuation(l, prev=None):
    """
    Check if l is a continuation line.

    l and prev must not be comment lines.
    """
    # If l has 5 or more leading spaces, it is a continuation independently
    # on prev
    if re_continuation.match(l):
        return True
    elif prev and '&' in prev:
        return True
    return False


if __name__ == '__main__':
    from sys import argv
    from blocks import get_block_positions
    text = open(argv[1]).read()

    dbi = get_block_positions(text)

    for b, (ii, l) in dbi.items():
        if b in 'csd':
            for c, n, t in get_cards(text[slice(*ii)]):
                print n + l, t, utils.shorten(c)
