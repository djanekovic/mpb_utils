import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
import math
import plot_script

num_bands = 8
resolution = 32
mesh_size = 7

geometry_lattice = mp.Lattice(size = mp.Vector3(1, 1))

k_points = [mp.Vector3(),
            mp.Vector3(x=0.5),
            mp.Vector3(1/2, 1/2),
            mp.Vector3()]
k_points = mp.interpolate(50, k_points)

default_material = mp.Medium(epsilon=12)

ms = mpb.ModeSolver(
        geometry_lattice = geometry_lattice,
        k_points = k_points,
        default_material = default_material,
        num_bands = num_bands,
        mesh_size = mesh_size,
        resolution = resolution)

r = 1.066
ms.geometry = [
        mp.Prism(vertices = [mp.Vector3(-r/2, -r/2), mp.Vector3(r/2, -r/2), mp.Vector3(y=r*0.5)],
                 material = mp.Medium(epsilon=1),
                 height = mp.inf)]
ms.run_tm()
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
ms.run_te()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list

plot_script.plot(tm_freqs, tm_gaps, te_freqs, te_gaps, name="triangle_holes_max_full.pdf", limit=0.5, save=True)

#md = mpb.MPBData(rectify=True, periods=3, resolution=32)
#eps = ms.get_epsilon()
#converted_eps = md.convert(eps)
#plt.imshow(converted_eps.T, interpolation='spline36', cmap='binary')
#plt.axis('off')
#plt.show()
