#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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

        for i, c in enumerate(self.__order):
            self.__setattr__(c, i)

    def __item__(self, i):
        return self.__order[i]


bid = BIDClass()


def get_blocks(text, start=None):
    """
    Returns a dictionary with separate blocks.
    """

    bld = re.compile('^\s*$', re.MULTILINE)

    # Blocks are separated by empty lines (except title and cells).
    bounds = []
    pos = 0
    while pos < len(text):
        pos = bld.search(text, pos + 1).start()
        bounds.append(pos)

    # Define the 1-st block
    # If the 1-st block is a message block, than if there is only two blocks,
    # this is a continue-run input and the second block is the data block. If
    # there are more than 2 blocks, this is a initial-run input and the first
    # block after the message block is the title-block.
    if is_message_block(text[0:bounds[0]]):
        if len(bounds) <= 2:
            b = 'd'
        else:
            b = 't'


    return bounds


def is_message_block(txt):
    """
    Checks if txt is a message block.
    """
    kw = txt[:50].split()[0].lower()
    return kw == 'message'


if __name__ == '__main__':
    txt = open('cmodel.inp', 'r').read()
    d = get_blocks(txt)
    for i in d:
        print repr(txt[i-10: i+10])
