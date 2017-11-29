# return dictionary describing cells
from collections import OrderedDict


def get_cells(input, lim=None):
    """
    input is an instance of mip.MIP class.
    """
    d = OrderedDict()
    n = 0
    for c in input.cards(blocks='c', skipcomments=True):
        name, mat, geom, opts = c.parts()
        name = int(name)
        d[name] = (mat, geom, opts)
        n += 1
        if lim and n > lim:
            break
    return d


def parse_mat(s):
    mat, den = (s + ' 0').split()[:2]
    mat = int(mat)
    if mat == 0:
        return (mat, )
    else:
        den = float(den)
        return (mat, den)


if __name__ == '__main__':
    from sys import argv
    from mcrp_splitters import InputSplitter

    i = InputSplitter(argv[1])
    d = get_cells(i, lim=None)
    print d.items()[0]
    print d.items()[-1]
    print len(d)
