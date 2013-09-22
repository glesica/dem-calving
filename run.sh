#!/bin/sh

# Clean up from previous runs
rm src/*.pyc
mkdir -p output
rm output/*.vtu
rm output/*.txt

# Run the packing simulation
mpirun -np 2 `which esysparticle` src/packer.py
dump2vtk -i output/settle-chk -o output/settle-vtk_ -t 0 1001 100

# Clean up after ourselves
rm src/*.pyc
rm output/*.txt
