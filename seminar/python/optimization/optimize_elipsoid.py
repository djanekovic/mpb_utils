#!/usr/bin/python3

import math
import meep as mp
from meep import mpb
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # This import has side effects required for the kwarg projection='3d' in the call to fig.add_subplot

def optimize_ellipsoid(a, b):
    ms.geometry = [mp.Ellipsoid(size=mp.Vector3(a, b, mp.inf),
                            material = mp.Medium(epsilon=1))]
    ms.run()
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


band_gaps_ellipsoid = []
plt.style.use('seaborn-white')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


x = y = np.linspace(0, 2, 50)
X, Y = np.meshgrid(x, y)
zs = np.array([optimize_ellipsoid(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)

ax.plot_surface(X, Y, Z)

ax.set_xlabel(r'\v{S}irina pravokutnika')
ax.set_ylabel(r'Du\v{z}ina pravokutnika')
ax.set_zlabel(r'$\Delta \omega / \omega_m$')

plt.show()
plt.savefig("optimize_elipsoid.pdf")

print (max(Z))
