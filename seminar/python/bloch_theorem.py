import meep as mp

resolution = 32
cell = mp.Vector3(16, 16, 0)
geometry = [mp.Cylinder(radius=0.2,
                        height = 1e20,
                        material = mp.Medium(epsilon=12))]

sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component = mp.Ez,
                     center = mp.Vector3(0, 8, 0))]

pml_layers = [mp.PML(1.0)]

sim = mp.Simulation(cell_size = cell,
                    boundary_layers = pml_layers,
                    geometry = geometry,
                    sources = sources,
                    resolution = resolution)

sim.run(until=200)
