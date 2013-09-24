#!/bin/bash

#
# Constants
#

PROGNAME=`basename $0`
 
#
# Helper Functions
#

# Error printer
function error_echo() {
    echo "${PROGNAME}: ${1:-"Unknown error"}" 1>&2
}
    
# Error output function
function error_exit() {
    error_echo "${1}"
    exit 1
} 

# Prepare for a new run, dump old outputs, etc.
function prepare_run() {
    rm src/*.pyc
    mkdir -p output
    rm output/*.vtu
    rm output/*.txt
}

# Cleanup after a run
function teardown_run() {
    rm src/*.pyc
    rm output/*.txt
}

# Prints useful help information
function help() {
    echo "Usage: ${PROGNAME} <n>"
    echo "    n : number of timesteps to run for"
}

#
# Primary Functions
#

function run_packer() {
    prepare_run

    # Run the packing simulation
    mpirun -np 2 `which esysparticle` src/packer.py ${NUM_TIMESTEPS}
    dump2vtk -i output/pack-chk -o output/pack-vtk_ -t 0 ${NUM_SNAPSHOTS} 1000

    teardown_run

    return 0
}

#
# Figure out what to run and do it
#

if [ -z "${2}" ]; then
    help
    error_exit "Error: number of timesteps ommitted"
fi
NUM_TIMESTEPS=${2}
NUM_SNAPSHOTS=`expr $NUM_TIMESTEPS / 1000 + 1`

case ${1} in
    "packer" ) run_packer;;
esac

exit ${?}
