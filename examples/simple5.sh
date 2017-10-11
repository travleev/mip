#!/bin/bash

rm simple5.inp? simple5.p*
mcnp5.mpi ip name=simple5.inp plot=simple5 com=simple5.cmd notek
ps2pdf simple5.ps

