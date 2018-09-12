#!/bin/bash

python3 optimize_ellipsoid.py &
python3 optimize_ellipsoid_2d.py &
wait
