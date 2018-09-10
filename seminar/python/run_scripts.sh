#!/bin/bash

python3	./1d_crystal.py &
python3 ./dielectric_rods_square_lattice.py &
python3 ./dielectric_rods_triangular_lattice.py &
python3 ./dielectric_holes_triangular_lattice.py &
wait

cp 1d_crystal_gap.pdf square_rods.pdf triangular_rods.pdf triangular_holes.pdf ../images/.
