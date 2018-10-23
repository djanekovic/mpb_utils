import meep as mp


def main():
    # Cell dimension
    ax, ay = 16, 16
    # Source location
    sx = 8
    sy = 15
    resolution = 32

    cell = mp.Vector3(ax, ay, 0)

    geometry = []
    for i in range(-ax//2, ax//2):
        for j in range(-ay//2, ay//2-2):
            geometry.append(mp.Cylinder(radius=0.2,
                            height = 1e20,
                            material = mp.Medium(epsilon=12),
                            center = mp.Vector3(i, j, 0)))

    sources = [mp.Source(mp.ContinuousSource(frequency=0.5),
                         component = mp.Ez,
                         center = mp.Vector3(0, ay/2-1, 0),
                         amplitude = 10)]

    pml_layers = [mp.PML(1.0)]

    sim = mp.Simulation(cell_size = cell,
                        boundary_layers = pml_layers,
                        geometry = geometry,
                        sources = sources,
                        resolution = resolution)

    sim.run(mp.at_beginning(mp.output_epsilon),
            mp.to_appended("ez", mp.at_every(0.3, mp.output_efield_z)),
            until=150)

if __name__ == "__main__":
    main()
