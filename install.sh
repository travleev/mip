#!/bin/bash 

# Install for developing
pip uninstall mip
pip install -e .

# Install on Windows:
# rm dist
# python setup.py sdist
# cd dist
# pip install mip.*zip