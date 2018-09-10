#!/usr/bin/python3

import math
import meep as mp
from meep import mpb
import numpy as np
import matplotlib.pyplot as plt

"""
    variraj r od 0 do sqrt(2)/2 ako je argument -c -> Cylinder
    variraj velicinu kvadrata 0 do 1 ako je arg -b -> Block
"""
def optimize_cylinder(r):
    ms.geometry = [mp.Cylinder(r, material = mp.Medium(epsilon=1))]
    ms.run()
    if len(ms.gap_list):
        return max(ms.gap_list)[0]
    return 0

def optimize_block(r):
    ms.geometry = [mp.Block(size=mp.Vector3(r, r),
                            material = mp.Medium(epsilon=1))]
    ms.run()
    if len(ms.gap_list):
        return max(ms.gap_list)[0]
    return 0

def optimize_elipsoid(a, b):
    ms.geometry = [mp.Elipsoid(size=mp.Vector3(a, b),
                            material = mp.Medium(epsilon=1))]
    ms.run()
    if len(ms.gap_list):
        return max(ms.gap_list)[0]
    return 0

num_bands = 5
resolution = 64

default_material = mp.Medium(epsilon = 12)

geometry_lattice = mp.Lattice(size = mp.Vector3(1, 1),
                              basis1 = mp.Vector3(0.5, math.sqrt(3)/2),
                              basis2 = mp.Vector3(0.5, -math.sqrt(3)/2))

k_points = [mp.Vector3(),               # Gamma
            mp.Vector3(0.5),            # M
            mp.Vector3(1/3, 1/3),       # K
            mp.Vector3()]               # Gamma

k_points = mp.interpolate(30, k_points)

ms = mpb.ModeSolver(geometry_lattice=geometry_lattice,
                    k_points=k_points,
                    resolution=resolution,
                    num_bands=num_bands,
                    default_material = default_material)


band_gaps_cylinder = []
band_gaps_block = []

plt.style.use('seaborn-white')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, ax = plt.subplots()

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


for r in np.linspace(0, math.sqrt(2)/2, 10):
    band_gaps_cylinder.append((r, optimize_cylinder(r)))

plt.plot(*zip(*band_gaps_cylinder))
ax.set_xlim(0, 1)
ax.set_ylim(0, 20)
plt.xlabel('Pulumjer [a]')
plt.ylabel(r'$\Delta \omega / \omega_m$')
plt.show()
