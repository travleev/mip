#!/bin/bash

rm simple6.inp? simple6.p*
mcnp5.mpi ip name=simple6.inp plot=simple6 com=simple6.cmd notek
ps2pdf simple6.ps

