#!/bin/bash

rm simple3.inp? simple3.p*
mcnp5.mpi ip name=simple3.inp plot=simple3 com=simple3.cmd notek
ps2pdf simple3.ps

