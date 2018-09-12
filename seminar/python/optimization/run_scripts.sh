#!/bin/bash

python3 optimize_cylinder.py &
python3 optimize_block.py &
python3 optimize_block_te.py &
wait
