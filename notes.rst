Set of loosely coupled packages
================================
Reading an MCNP input file is an essential part of many applications. To some
extent, it was implemented in PIRS. Later it turned out that the PIRS
implementation is not suitable for the purposes of numjuggler, therefore the
latter one has its own implementaiton. Reading information from the input file
is also important for R2S, which can make use of the PIRS reader, but I don't
like the idea to make dependence on PIRS (sinse it is not maintained and broken
in some parts).

Instead, there should be a set of packages related to work with MCNP, each doing
a well-defined piece of work, with its own version number.

For example, all MCNP text files can become large and there should be methods to
split them into chunks that are more simple to handle. Such methods can be than 
used in many other places (PIRS, numjuggler, R2S, CAD converter).

Ther should ba naming convention for the packages. Current proposal (that takes
into account requirements/suggestions for PyPI) is to use a prefix ``mcrp-``
standing for "MCNP-related packages", followed by a particular name of the
package. For example, the text file splitters can be described in the
``mcrp-splitters``. The renumbering tool can be disctibuted with the
``mcrp-numjuggler`` package and the CAD converter -- as ``mcrp-2cad``.


