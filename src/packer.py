"""
packer.py

Settling simulation to generate a low-energy packing.
"""

import sys
from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *
from runnables import ParticleAdder

if len(sys.argv) < 2:
    sys.stderr.write('Error: number of timesteps ommitted\n')
    sys.exit(1)

NUM_TIMESTEPS = int(sys.argv[1])

SPATIAL_XMIN = 0
SPATIAL_XMAX = 10
SPATIAL_YMIN = 0
SPATIAL_YMAX = 10
SPATIAL_ZMIN = 0
SPATIAL_ZMAX = 10

MESH_NAME = 'cube10x10x10'
MESH_DIR = 'src/meshes'

MIN_RADIUS = 0.25
MAX_RADIUS = 0.75
MIN_MASS = MIN_RADIUS
MAX_MASS = MAX_RADIUS

GRAVITY_MAGNITUDE = 10
VISCOSITY = 2.5

sim = LsmMpi(
        numWorkerProcesses=1,
        mpiDimList=[1, 1, 1])
sim.initNeighborSearch(
        particleType='NRotSphere',
        gridSpacing=2.5,
        verletDist=0.1)

sim.setNumTimeSteps(NUM_TIMESTEPS)
sim.setTimeStepSize(1.0e-04)

sim.setSpatialDomain(
        BoundingBox(
            Vec3(SPATIAL_XMIN, SPATIAL_YMIN, SPATIAL_ZMIN),
            Vec3(SPATIAL_XMAX, SPATIAL_YMAX, SPATIAL_ZMAX)))

sim.readMesh(fileName=MESH_DIR + '/' + MESH_NAME + '.msh',
        meshName=MESH_NAME)

sim.createInteractionGroup(
        NRotFrictionPrms(
            name='friction',
            normalK=1000.0,
            dynamicMu=0.6,
            shearK=100.0,
            scaling=True))

sim.createInteractionGroup(
        NRotElasticPrms(
            name='repel',
            normalK=1.0e3,
            scaling=True))

sim.createInteractionGroup(
        NRotElasticTriMeshPrms(
            name='mesh-repel',
            meshName=MESH_NAME,
            normalK=1.0e6))

sim.createInteractionGroup(
        GravityPrms(
            name='gravity',
            acceleration=Vec3(0.0, -GRAVITY_MAGNITUDE, 0.0)))

sim.createInteractionGroup(
        LinDampingPrms(
            name='viscosity',
            viscosity=VISCOSITY,
            maxIterations=100))

adder = ParticleAdder(sim, 1000,
        xdomain=(SPATIAL_XMIN + MAX_RADIUS, SPATIAL_XMAX - MAX_RADIUS),
        ydomain=(SPATIAL_YMAX, SPATIAL_YMAX),
        zdomain=(SPATIAL_ZMIN + MAX_RADIUS, SPATIAL_ZMAX - MAX_RADIUS),
        radrange=(MIN_RADIUS, MAX_RADIUS),
        massrange=(MIN_MASS, MAX_MASS))
sim.addPreTimeStepRunnable(adder)

sim.createCheckPointer(
        CheckPointPrms(
            fileNamePrefix='output/pack-chk',
            beginTimeStep=0,
            endTimeStep=NUM_TIMESTEPS,
            timeStepIncr=1000))

sim.run()
