#!/usr/bin/python3

import math
import meep as mp
from meep import mpb
from plot_script import plot
import matplotlib.pyplot as plt

num_bands = 15
resolution = 32

r=0.7931
epsilon = 1
default_material = mp.Medium(epsilon = 12)

geometry = [mp.Block(size = mp.Vector3(r, r, mp.inf), material=mp.Medium(epsilon=epsilon))]
geometry_lattice = mp.Lattice(size = mp.Vector3(1, 1),
                              basis1 = mp.Vector3(0.5, math.sqrt(3)/2),
                              basis2 = mp.Vector3(0.5, -math.sqrt(3)/2))

k_points = [mp.Vector3(),               # Gamma
            mp.Vector3(0.5),            # M
            mp.Vector3(1/3, 1/3),       # K
            mp.Vector3()]               # Gamma

k_points = mp.interpolate(100, k_points)

ms = mpb.ModeSolver(geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    k_points=k_points,
                    resolution=resolution,
                    num_bands=num_bands,
                    default_material = default_material)

ms.geometry = [mp.Block(size=mp.Vector3(r, r, mp.inf),
                        material = mp.Medium(epsilon=1))]
ms.run_tm()
tmfreq = ms.all_freqs
tmgaps = ms.gap_list
ms.run_te()
tefreq = ms.all_freqs
tegaps = ms.gap_list

md = mpb.MPBData(rectify=True, periods=3, resolution=32)
eps = ms.get_epsilon()
converted_eps = md.convert(eps)
plt.imshow(converted_eps.T, interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

plot(tmfreq, tmgaps, tefreq, tegaps, name="triangular_squares_te_max.pdf", save=True)
