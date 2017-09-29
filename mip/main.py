
from blocks import get_block_positions
from cards import get_cards


import re
import cellcard
import surfacecard
import datacard

re_comment = re.compile('[$&].*$', re.MULTILINE)
re_spaces = re.compile('\s+')

class Card(object):
    def __init__(self, lines=[], position=0, type=None):
        self.lines = lines
        self.position = position
        self.type = type
        return

    def content(self):
        """
        return one line containing only meaningful part of the card.


        From a list of lines representing a card with comments, extract only
        meaningfull part (i.e. remove all comments and extra-spaces). The result is
        a one-line string.

        It is assumed that 1-st and last lines in the list are not comment lines
        (i.e.  that this text is obtained from
        cards.get_cards(skipcomments=True) generator.
        """

        # Remove in-line comments denoted by $ or &
        res = []
        for l in self.lines:
            res.extend(re_comment.split(l))

        # Remove multiple spaces
        res = ' '.join(res)
        res = re_spaces.sub(' ', res)
        return res

    def parts(self):
        if self.type == 'c':
            name, mat, geom, opts = cellcard.split_cell_card(self.content())
            return name, mat, geom, opts

        if self.type == 's':
            name, tr, typ, params = surfacecard.split(self.content())
            return name, tr, typ, params

        if self.type == 'd':
            typ, name, params = datacard.split(self.content())
            return name, typ, params
        else:
            raise NotImplementedError


class MIP(object):
    def __init__(self, fname, firstblock=None):

        # Text from the input file
        self.text = open(fname, 'r').read()

        # Dictioary of indices describing position of blocks
        self.bi = get_block_positions(self.text, firstblock=firstblock)

        return

    def block(self, bid):
        ii, l = self.bi[bid]
        return l, self.text[slice(*ii)]

    def blocks(self, blocks='mtcsd'):
        for b in blocks:
            if b in self.bi:
                ii, l = self.bi[b]
                yield b, l, self.text[slice(*ii)]

    def cards(self, blocks='csd', skipcomments=False):
        for b, n0, txt in self.blocks(blocks):
            for c, n, t in get_cards(txt, skipcomments=skipcomments):
                if t == 'card':
                    t = b
                yield Card(lines=c, position=n0 + n, type=t)


if __name__ == '__main__':
    from sys import argv
    import utils

    input = MIP(argv[1])

    # print blocs
    for b, l, txt in input.blocks():
        print b, l, utils.shorten(repr(txt))

    # split cards to parts
    for c in input.cards(blocks='csd', skipcomments=True):
        print '*'*60
        print c.position
        print c.content()
        print c.parts()
