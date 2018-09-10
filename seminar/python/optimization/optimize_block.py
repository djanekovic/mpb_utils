#!/usr/bin/python3

import math
import meep as mp
from meep import mpb
import numpy as np
import matplotlib.pyplot as plt

"""
    variraj velicinu kvadrata 0 do 1 ako je arg -b -> Block
"""
def optimize_block(r):
    ms.geometry = [mp.Block(size=mp.Vector3(r, r, mp.inf),
                            material = mp.Medium(epsilon=1))]
    ms.run_te()
    if len(ms.gap_list):
        return max(ms.gap_list)[0]
    return 0


num_bands = 5
resolution = 32

default_material = mp.Medium(epsilon = 12)

geometry_lattice = mp.Lattice(size = mp.Vector3(1, 1),
                              basis1 = mp.Vector3(0.5, math.sqrt(3)/2),
                              basis2 = mp.Vector3(0.5, -math.sqrt(3)/2))

k_points = [mp.Vector3(),               # Gamma
            mp.Vector3(0.5),            # M
            mp.Vector3(1/3, 1/3),       # K
            mp.Vector3()]               # Gamma

k_points = mp.interpolate(20, k_points)

ms = mpb.ModeSolver(geometry_lattice=geometry_lattice,
                    k_points=k_points,
                    resolution=resolution,
                    num_bands=num_bands,
                    default_material = default_material)


band_gaps_block = []

plt.style.use('seaborn-white')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, ax = plt.subplots()

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


for r in np.linspace(0, 1, 30):
    band_gaps_block.append((r, optimize_block(r)))

plt.plot(*zip(*band_gaps_block))
ax.set_xlim(0, 1)
#ax.set_ylim(0, 2)
plt.xlabel('Dimenzije osnovne stranice kvadrata [a]', size=16)
plt.ylabel(r'$\Delta \omega / \omega_m$', size=16)
plt.savefig("optimization_block_te.pdf")

print (max(band_gaps_block, key=lambda x: x[1]))
