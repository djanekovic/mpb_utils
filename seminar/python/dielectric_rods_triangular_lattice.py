#!/usr/bin/python3

import math
import meep as mp
from meep import mpb
from plot_script import plot

num_bands = 8
resolution = 32

# variables: r, epsilon
r=0.2
epsilon = 12
geometry = [mp.Cylinder(r, material=mp.Medium(epsilon=epsilon))]
geometry_lattice = mp.Lattice(size = mp.Vector3(1, 1),
                              basis1 = mp.Vector3(0.5, math.sqrt(3)/2),
                              basis2 = mp.Vector3(0.5, -math.sqrt(3)/2))

k_points = [mp.Vector3(),               # Gamma
            mp.Vector3(0.5),            # M
            mp.Vector3(1/3, 1/3),       # K
            mp.Vector3()]               # Gamma

k_points = mp.interpolate(30, k_points)

ms = mpb.ModeSolver(geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    k_points=k_points,
                    resolution=resolution,
                    num_bands=num_bands)

ms.run_tm()
tmfreqs = ms.all_freqs
tmgaps = ms.gap_list
ms.run_te()
tefreqs = ms.all_freqs
tegaps = ms.gap_list

plot(tmfreqs, tmgaps, tefreqs, tegaps, name="triangular_rods.pdf", save=True)
