#!/urs/bin/env python
-*- coding: utf-8 -*-

"""
Split cell card in name, material, geometry and options.

A cells card always starts with its name followed by one or more spaces. The
rest has two forms:

    * "LIKE n but ..." form. Here the keywords "like" and "but" are delimited by
    space(s).  The "but" keyword is followed by optional paramters, including
    those using parentheses (trcl, fill) and multiple entries (fill in presence
    of lat).

    * Material (one or two entires delimited by one or more spaces), followed by
    geometry description where entries can be delimited by spaces, colon and
    parentheses, followed by optional parameters (like in the "like n but"
    form).

Therefore, the cell name (number) is always delimited from the following part by
space(s).  The "like n but" entries also delimited by spaces. But geometry
description part can be delimited from the material part and the part containing
optional parameters with both space(s) and parentheses.

The part with optional parameters starts with an alphabet character. It
preceeded with a number followed by one or more space, or closing parenthesis,
followed by zero or more spaces.

"""

import re

re_likebut = re.compile(r"""^(\s*[0-9]+)     # name
                             (\s+like.*but)  # like-but geometry
                             (.*)$  i        # the rest -- options """,
                        re.IGNORECASE, re.VERBOSE)
re_void = re.compile(r"""^(\s*[0-9]+)       # name
                          (\s+\S+)          # zero material
                          ([)(0-9\s:#-+])   # geometry
                          (.*)$             # rest -- options""",
                     re.IGNORECASE, re.VERBOSE)
re_nonvoid = re.compile(r"""^(\s*[0-9]+)       # name
                             (\s+\S+\s+\S+)    # material and density
                             ([)(0-9\s:#-+])   # geometry
                             (.*)$             # rest -- options""",
                     re.IGNORECASE, re.VERBOSE)

def split_cell_card(txt):
    """
    Split cell card txt into parts.

    String `txt` must have no comments and new-line characters.
    """
    name, tn, trest = txt.split(None, 2)
    if tn.lower() == 'like':
        name, geom, opts = re_likebut.findall(txt)[0]
        mat = ''
    elif float(tn) == 0.0:
        name, mat, geom, opts = re_void.findall(txt)[0]
    else:
        name, mat, geom, opts = re_nonvoid.findall(txt)[0]
    return name, mat, geom, opts

