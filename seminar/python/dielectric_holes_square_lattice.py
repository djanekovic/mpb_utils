#!/usr/bin/python3

import math
import os
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
import plot_script

num_bands = 8
resolution = 32
geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1))

default_material = mp.Medium(epsilon=12)

geometry = [mp.Block(size=mp.Vector3(0.88, 0.88),
                     material=mp.Medium(epsilon=1))]
k_points = [mp.Vector3(),               # Gamma
            mp.Vector3(0.5),            # M
            mp.Vector3(1 / 2, 1 / 2),   # K
            mp.Vector3(),               # Gamma
           ]
k_points = mp.interpolate(10, k_points)

ms = mpb.ModeSolver(geometry=geometry,
                    default_material = default_material,
                    geometry_lattice=geometry_lattice,
                    k_points=k_points,
                    resolution=resolution,
                    num_bands=num_bands)

ms.run_tm()
tmfreq = ms.all_freqs
tmgaps = ms.gap_list
ms.run_te()
tefreq = ms.all_freqs
tegaps = ms.gap_list

plot_script.plot(tmfreq, tmgaps, tefreq, tegaps, name = "../images/pdf/square_lattice_holes_band_diagram.pdf", save=False)
