import meep as mp
from meep import mpb
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar

def optimize_bandgap(r):
    ms.geometry = [
            mp.Prism(vertices = [mp.Vector3(-r/2, -r/2), mp.Vector3(r/2, -r/2), mp.Vector3(y=r*0.5)],
                     material = mp.Medium(epsilon=1),
                     height = mp.inf)]
    ms.run()
    if len(ms.gap_list):
        return max(ms.gap_list)[0]
    return 0


num_bands = 8
resolution = 32
mesh_size = 7

geometry_lattice = mp.Lattice(size = mp.Vector3(1, 1))

k_points = [mp.Vector3(),
            mp.Vector3(x=0.5),
            mp.Vector3(1/2, 1/2),
            mp.Vector3()]
k_points = mp.interpolate(20, k_points)

default_material = mp.Medium(epsilon=12)

ms = mpb.ModeSolver(
        geometry_lattice = geometry_lattice,
        k_points = k_points,
        default_material = default_material,
        num_bands = num_bands,
        mesh_size = mesh_size,
        resolution = resolution)

draw = 1
if (draw):
    band_gaps_custom = []

    plt.style.use('seaborn-white')
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    fig, ax = plt.subplots()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for x in np.linspace(0.8, 1.6, 50):
        band_gaps_custom.append((x, optimize_bandgap(x)))

    print (band_gaps_custom)
    plt.plot(*zip(*band_gaps_custom))
    plt.xlabel('Dimenzije osnovne stranice trokuta [a]', size=16)
    plt.ylabel(r'Postotak fotoni\v{c}kog zabranjenog pojasa [\%]', size=16)
    plt.grid(False)
    plt.savefig("triangle_optimization.pdf", bbox_inches = 'tight')

    print (max(band_gaps_custom, key=lambda x: x[1]))
else:
    result = minimize_scalar(optimize_bandgap,  bounds=(0, 1), tol=0.1)
    print("radius at maximum: {}".format(result.x))
    print("gap size at maximum: {}".format(result.fun * -1))

#md = mpb.MPBData(rectify=True, periods=3, resolution=32)
#eps = ms.get_epsilon()
#converted_eps = md.convert(eps)
#plt.imshow(converted_eps.T, interpolation='spline36', cmap='binary')
#plt.axis('off')
#plt.show()
