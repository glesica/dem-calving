#!/bin/sh

# Clean up from previous runs
rm src/*.pyc
mkdir -p output
rm output/*.vtu
rm output/*.txt

# Read in parameters
if [ -z "${1}" ]; then
    echo "Error: number of timesteps ommitted" 1>&2
    exit 1
fi
NUM_TIMESTEPS=${1}
NUM_SNAPSHOTS=`expr $NUM_TIMESTEPS / 100 + 1`

# Run the packing simulation
mpirun -np 2 `which esysparticle` src/packer.py ${NUM_TIMESTEPS}
dump2vtk -i output/pack-chk -o output/pack-vtk_ -t 0 ${NUM_SNAPSHOTS} 100

# Clean up after ourselves
rm src/*.pyc
rm output/*.txt
