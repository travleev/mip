
"""
Geometry model is represented by two dictionaries.

One dictionary contains cells, with geometry parsed to ast.

The other dictionary contains surfaces, mentioned in the cells.
"""

from surfaces import get_surfaces
from cells import get_cells
from parsegeom import get_ast, modify_ast


def get_geom(i, lim=None):
    cells = get_cells(i, lim=lim)
    surfs = get_surfaces(i)

    for k, v in cells.items():
        mat, geom, opts = v
        ast = get_ast(geom)
        cells[k] = ast

    return cells, surfs


if __name__ == '__main__':
    from sys import argv
    from mip import MIP
    from testgrammar import pprint_dict

    i = MIP(argv[1])
    cd, sd = get_geom(i, lim=10)
    for k, ast in cd.items():
        print 'cell', k
        c = modify_ast(ast, sd)
        print '\n'.join(pprint_dict(c))
