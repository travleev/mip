#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import utils

"""
Split MCNP input file to blocks.

A working MCNP input file can have from 1 to 5 blocks:

    -------------       -----------------
    initial run         continue run
    -------------       -----------------
    message*            message*

    title               data
    cells

    surfaces

    data*
    -------------       -----------------

Also there could be situations that only part of an input file is
supplied for parsing. In this case the user must specify what block
the part starts with.

"""


class BIDClass(object):
    """
    BLock ID.

    Represetns block names and IDs. Only single instance is needed.
    """
    def __init__(self):
        # Order of blocks in input file:
        #   message
        #   title
        #   cells
        #   surfaces
        #   data
        self.__order = 'mtcsd'

        self.m = 0
        self.t = 1
        self.c = 2
        self.s = 3
        self.d = 4

    def __getitem__(self, i):
        return self.__order[i]


bid = BIDClass()


def get_block_positions(text, firstblock=None):
    """
    Returns a dictionary with tuple of indices that identify block begin and
    end.
    """

    # Resulting dictionary
    dres = {}

    # Regular expresison for blank line delimiter
    bld = re.compile('^\s*$', re.MULTILINE)

    # Re.split() does not split on empty matches. Therefore, match positions
    # are searched and blocks are build manually.
    bi = []
    ps = 0  # block start position
    while ps < len(text):
        # match.start() returns index of the 1-st character of the found match,
        # in case of bld this is the next char  after the 1-st \n.
        pe = bld.search(text, ps).start()
        bi.append((ps, pe))
        ps = pe + 1

    # Line count. Starts form 1, to be consistent with vim's G
    line = 1
    # Check if message block exists
    if text[:20].split()[0].lower() == 'message:':
        dres['m'] = bi[0], line
        line += number_of_lines(txt, *bi[0])
        bi.pop(0)

    # Define type of the first block, if not given explicitly
    if firstblock is None:
        if len(bi) == 1:
            firstblock = bid.d
        else:
            firstblock = bid.t
            i1, i2 = split_line_index(text, bi[0][0])
            bi.insert(0, (bi[0][0], i1))
            bi[1] = (i2, bi[1][1])

    cb = firstblock
    while bi:
        dres[bid[cb]] = bi[0], line
        line += number_of_lines(text, *bi[0])
        bi.pop(0)
        cb += 1

    return dres


def split_line_index(mlstring, start=0):
    """
    Return two indices, for the end of the 1-st line and start of the next one.
    """
    r = re.compile('[\r\n]+')
    m = r.search(mlstring, start)
    return m.start(), m.end()


def number_of_lines(txt, start=None, end=None):
    """
    Return number of lines in the multi-line string txt.
    """
    if start is None:
        start = 0
    if end is None:
        end = len(txt)
    if '\r' in txt:
        return txt.count('\r', start, end) + 1
    else:
        return txt.count('\n', start, end) + 1


if __name__ == '__main__':
    from sys import argv
    txt = open(argv[1], 'r').read()
    d = get_block_positions(txt)
    for k, (ii, l) in d.items():
        s = txt[slice(*ii)]
        print k, l, utils.shorten(s)
