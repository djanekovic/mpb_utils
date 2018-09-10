#!/usr/bin/python3
import math
import os
import meep as mp
from meep import mpb
from plot_script import plot
import argparse

num_bands = 2;

k_points = [mp.Vector3(-0.5), mp.Vector3(0.5)]
k_points = mp.interpolate(200, k_points)

# Block is in center with dimensions (1/3, 1)
geometry = [mp.Block(size=mp.Vector3(1/3, 1),
                     material = mp.Medium(epsilon=12))]

geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1))

resolution = 32

ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

ms.run_tm()
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
ms.run_te()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list

plot(tm_freqs, tm_gaps, te_freqs, te_gaps, name="1d_crystal_gap.pdf", limit=0.5, save=True)
