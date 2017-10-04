
# setuptools should be used for both Python 3 and Python 2, see
# https://docs.python.org/2.7/library/distutils.html#module-distutils
# from distutils.core import setup
from setuptools import setup, find_packages


setup(name='mip',
      # version: X.Y.Z, where:
      #    X -- major version. Different major versions are not back-compatible.
      #         New major version number, when code is rewritten
      #
      #    Y -- minor version. New minor version, when new function(s) added.
      #
      #    Z -- update, new update number when a bug is fixed.
      version='0.0a.0',
      description='MCNP input file parser',
      author='A.Travleev',
      author_email='anton.travleev@kit.edu',
      packages=find_packages('.'),  #  ['mip', 'geom'],
      package_dir={'': '.'},
      package_data={'geom': ['grammars/*.ebnf']},
      # include_package_data=True,
      )
