# Return dictionary describing transformations
from collections import OrderedDict

def get_transforms(input, lim=None):
    """
    input is an instance of mpi.MIP class.
    """
    d = OrderedDict()
    n = 0
    for c in input.cards(blocks='d', skipcomments=True):
        name, dtype, params = c.parts()
        if dtype.lower() == 'tr':
            name = int(name)
            d[name] = params
            n += 1
            if lim and n > lim:
                break
    return d





