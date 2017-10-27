#!/bin/bash

rm simple7.inp? simple7.p*
mcnp5.mpi ip name=simple7.inp plot=simple7 com=simple7.cmd notek
ps2pdf simple7.ps

