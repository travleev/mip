# Test ability to import modules from ../geom and ../mip.

# Relative imports will not work, if the current file is executed as the main.
# The SC python interpreter has only 3 entries in sys.path, which do not include
# path to the site-packages of the system's python. This means that if a script
# in SC needs a 3-rd package, this package must be installed into the SC-specific
# folder, which is SC version dependent. ALternytively, the SC script can modify
# at the begin the sys.path list in order to include standard python places. For
# example, by appending (insertion to the 1-st position is not necessary) the 
# `PYTHONPATH` variable. This variable is anyway worth to define in windows.

from os import environ
import sys

sys.path.insert(0, environ['PYTHONPATH'])
for p in sys.path: print p

import geom.main
import geom.forcad

fname = r'D:\github\mip\examples\simple2.inp'

cd, sd, td = geom.main.get_geom(fname)
cads, wr = geom.forcad.translate(sd, td)

for k, v in cads.items(): 
    print k
    print v
print wr











d, td = geom.main.get_geom(fname)
cads, wr = geom.forcad.translate(sd, td)











