#!/usr/bin/python3

import math
import meep as mp
from meep import mpb
import numpy as np
import matplotlib.pyplot as plt

def optimize_triangle(r):
    vertices = [mp.Vector3(0, 1*r),
                mp.Vector3(r*math.sqrt(3)/2, -r/2),
                mp.Vector3(-r*math.sqrt(3)/2, -r/2)]
    ms.geometry = [mp.Prism(vertices = vertices,
                            height = mp.inf,
                            center = mp.Vector3(),
                            material = mp.Medium(epsilon=1))]
    ms.run()
    if len(ms.gap_list):
        return max(ms.gap_list)[0]
    return 0

num_bands = 15
resolution = 32

default_material = mp.Medium(epsilon = 13)

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


band_gaps_triangle = []

plt.style.use('seaborn-white')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, ax = plt.subplots()

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for r in np.linspace(0.01, math.sqrt(3)/3, 20):
    band_gaps_triangle.append((r, optimize_triangle(r)))

print (band_gaps_triangle)
plt.plot(*zip(*band_gaps_triangle))
ax.set_xlim(0, 1)
ax.set_ylim(0, 2)
plt.xlabel('Duljina stranice [a]')
plt.ylabel(r'$\Delta \omega / \omega_m$')
plt.grid(False)
plt.show()
