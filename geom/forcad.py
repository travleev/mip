"""
Prepare parameters for creatiing surfaces in CAD.

Each function gets as argument the ist of parameters of the correspondent MCNP
surface card.  returned is a tuples describing frame, set of parameters and the
point 'below' the surface.

Transformation can be applied to the result of that functions.

Point to identify the negative-sense part must be inside the world. Since the
size of the world has no influence to CAD generation time, it can be set
arbitrarily large. For example, to ensure that all 'below'-points for particular
surface are inside the world. In this case, definition of the 'below'-points is
much more simple.

The length of the rasius-vector to the most extending 'below'-point in the model
defines the world's radius. The center of the world is at the coordinate origin.

The world's center can be improved by searching min/max values of x, y and z
used in definition of the MCNP surfaces (similar to definition of the source for
volume calculations in numjuggler).

"""

from math import atan

# module main entry. This is a dictionary of functions that take MCNP surface
# parameters and return parameters needed to build CAD surface.
mcnp2cad = {}

# Offset to define a point 'below' a surface
_offset = 1.0


def _shift(x, y, z, A, B, C, d):
    """
    Shift point p=(x, y, z) along n=(A, B, C) to distance d.

    It is assumed that |n| = 1. In many cases I define coordinates of n manually
    and than know in advance that they are normalized. Do not computing
    normalization here helps to save this computation for these case.
    """
    xx = x + A*d
    yy = y + B*d
    zz = z + C*d
    return (xx, yy, zz)


def _norm2(x, y, z):
    return x**2 + y**2 + z**2


def _norm(x, y, z):
    return _norm2(x, y, z)**0.5


def _sphere(x, y, z, R):
    frm = ((x, y, z), (0, 0, 1))
    srf = (R, )
    pin = (x, y, z)
    # Here and below: wrad is world radius assessment for current surface
    wrad = _norm(x, y, z) + R + _offset
    return frm, srf, pin, wrad


def _plane(x, y, z, A, B, C):
    """
    Plane throught the point (x, y, z) with the normal (A, B, C). The latter
    must be normalized to have unit length.
    """
    frm = ((x, y, z), (A, B, C))
    srf = ()
    pin = _shift(x, y, z, A, B, C, -_offset)
    wrad = _norm(x, y, z) + _offset
    return frm, srf, pin, wrad


def _cylinder(x, y, z, r, A, B, C):
    frm = ((x, y, z), (A, B, C))
    srf = (r, )
    pin = (x, y, z)
    wrad = _norm(x, y, z) + r + _offset
    return frm, srf, pin, wrad


def _cone(x, y, z, tana, A, B, C):
    """
    x, y, z -- cone focus coordinates,
    A, B, C -- cone axis direction, normalized to unit length
    tana -- tan of the angle

    CAD requries a point on the axis not coincident with the focus.
    """
    p = _shift(x, y, z, A, B, C, _offset)
    frm = (p, (A, B, C))
    srf = (tana*_offset, atan(tana))
    wrad = _norm(x, y, z) + tana*_offset + _offset
    return frm, srf, p, wrad


################################################################################
def so(p):
    """
    Sphere defined by `so` surface.
    """
    return _sphere(0, 0, 0, p[0])


def sx(p):
    """
    Sphere defined by `sx` surface.
    """
    return _sphere(p[0], 0, 0, p[1])


def sy(p):
    """
    Sphere defined by `sy` surface.
    """
    return _sphere(0, p[0], 0, p[1])


def sz(p):
    """
    Sphere defined by `sz` surface.
    """
    return _sphere(0, 0, p[0], p[1])


def s(p):
    """
    Sphere defined by `s` surface.
    """
    return _sphere(*p)


def px(p):
    """
    Plane defined by `px` sufrace.
    """
    return _plane(p[0], 0, 0, 1, 0, 0)


def py(p):
    """
    Plane defined by `py` sufrace.
    """
    return _plane(0, p[0], 0, 0, 1, 0)


def pz(p):
    """
    Plane defined by `pz` sufrace.
    """
    return _plane(0, 0, p[0], 0, 0, 1)


def p(p):
    """
    Plane defined by `p` surface.

    The MCNP plane is defined with parameters A, B, C, D of the plane equation

        (1) Ax + By + Cz - D = 0

    From these parameters, a point lying on the plane and the normal vector to
    the plane must be found.

    Multiplying coefficients A, B, C and D by arbitrary non-zero scalar does not
    change the above equation, therefore the parameters in the MCNP surface
    card can be defined to a arbitrary non-zero constant. In the following we
    assume that the normalization holds:

        A**2 + B**2 + C**2 = 1.

    Let the plane be defined by the point p0 and the normal vector n. An
    arbitrary point p lies on the plane, if the following equation is satisfied:

        (p - p0, n) = 0,  or
        (p, n) - (p0, n) = 0

    In the rectangular coordinate system, p=(x, y, z) and the above can be
    written as

        x nx + y ny + z nz - (p0, n) = 0

    Comparing this with (1) we find n and equation to p0 in terms of the MCNP
    parameters:

        (2) n = (A, B, C)
        (3) D = (p0, n)
              = x0 A + y0 B + z0 C

    The second equation does not define p0 uniquely. Additionally, we impose
    that p0 is the closest point to the oordinate's origin, i.e. the projection
    of (0, 0, 0) onto the plane. This point is

        p0 = n/|n| d,

    where d is the distance from (0, 0, 0) to the plane. Inserting this into (3)
    we obtain expression for d:

        (p0, n) = d/|n| (n, n) = D, or

        d = D|n|/(n, n) = D/|n|

    Inserting this to the expression for p0, we obtain:

        p0 = n D/(n, n)
    """
    # normalize parameters:
    A, B, C, D = p
    c = _norm(A, B, C)
    A = A/c
    B = B/c
    C = C/c
    D = D/c
    # Point on the plane
    x, y, z = _shift(0, 0, 0, A, B, C, D)
    return _plane(x, y, z, A, B, C)


def cz(p):
    """
    Cylinder defined by `cz` surface.
    """
    return _cylinder(0, 0, 0, p[0], 0, 0, 1)


def cy(p):
    """
    Cylinder defined by `cy` surface.
    """
    return _cylinder(0, 0, 0, p[0], 0, 1, 0)


def cx(p):
    """
    Cylinder defined by `cx` surface.
    """
    return _cylinder(0, 0, 0, p[0], 1, 0, 0)


def c_z(p):
    """
    Cylinder defined by `c/z` surface.
    """
    return _cylinder(p[0], p[1], 0, p[2], 0, 0, 1)


def c_y(p):
    """
    Cylinder defined by `c/y` surface.
    """
    return _cylinder(p[0], 0, p[1], p[2], 0, 1, 0)


def c_x(p):
    """
    Cylinder defined by `c/x` surface.
    """
    return _cylinder(0, p[0], p[1], p[2], 1, 0, 0)


def kz(p):
    """
    Cone defined by `kz` surface.
    """
    return _cone(0, 0, p[0], p[1]**0.5, 0, 0, 1)


def ky(p):
    """
    Cone defined by `ky` surface.
    """
    return _cone(0, p[0], 0, p[1]**0.5, 0, 1, 0)


def kx(p):
    """
    Cone defined by `kx` surface.
    """
    return _cone(p[0], 0, 0, p[1]**0.5, 1, 0, 0)


def k_x(p):
    """
    Cone defined by `k/x` surface.
    """
    return _cone(p[0], p[1], p[2], p[3]**0.5, 1, 0, 0)


def k_y(p):
    """
    Cone defined by `k/y` surface.
    """
    return _cone(p[0], p[1], p[2], p[3]**0.5, 0, 1, 0)


def k_z(p):
    """
    Cone defined by `k/z` surface.
    """
    return _cone(p[0], p[1], p[2], p[3]**0.5, 0, 0, 1)


mcnp2cad['so'] = so
mcnp2cad['sx'] = sx
mcnp2cad['sy'] = sy
mcnp2cad['sz'] = sz
mcnp2cad['s'] = s
mcnp2cad['px'] = px
mcnp2cad['py'] = py
mcnp2cad['pz'] = pz
mcnp2cad['p'] = p
mcnp2cad['cx'] = cx
mcnp2cad['cy'] = cy
mcnp2cad['cz'] = cz
mcnp2cad['c/x'] = c_x
mcnp2cad['c/y'] = c_y
mcnp2cad['c/z'] = c_z
mcnp2cad['kx'] = kx
mcnp2cad['ky'] = ky
mcnp2cad['kz'] = kz
mcnp2cad['k/x'] = k_x
mcnp2cad['k/y'] = k_y
mcnp2cad['k/z'] = k_z


def translate(surfaces, transform):
    """
    Return a dictionary of surfaces, suitable for passing to CAD.
    """
    Rw = 0.  # world radius.
    res = surfaces.__class__()  # surfaces can be an OrderedDict
    for k, v in surfaces.items():
        tr, stype, pl = v
        f, s, p, rw = mcnp2cad[stype](pl)
        # TODO apply transformation here to f and p
        res[k] = stype, f, s, p
        if Rw < rw:
            Rw = rw
    return res, Rw


# if __name__ == '__main__':
#     from sys import argv
#     from mip import MIP
#     from main import get_geom
#
#     cd, sd, td = get_geom(MIP(argv[1]))
#     cads, rw = translate(sd, td)
#     for k, v in cads.items():
#         stype, frm, srf = v
#         print k, stype, frm, srf
#     print 'Worlds radius', rw
