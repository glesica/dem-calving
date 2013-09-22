"""
settle.py

Settling simulation to generate a low-energy packing.
"""

from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *
from runnables import ParticleAdder

NUM_TIMESTEPS = 100000

SPATIAL_XMIN = -6
SPATIAL_XMAX = 6
SPATIAL_YMIN = -6
SPATIAL_YMAX = 6
SPATIAL_ZMIN = -6
SPATIAL_ZMAX = 6

MESH_NAME = 'cube'
MESH_DIR = 'src/meshes'

MIN_RADIUS = 0.25
MAX_RADIUS = 0.75
MIN_MASS = MIN_RADIUS
MAX_MASS = MAX_RADIUS

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
            acceleration=Vec3(0.0, -50.0, 0.0)))

sim.createInteractionGroup(
        LinDampingPrms(
            name='viscosity',
            viscosity=0.1,
            maxIterations=100))

adder = ParticleAdder(sim, 1000,
        xdomain=(-3.5, 3.5),
        ydomain=(4, 4),
        zdomain=(-3.5, 3.5),
        radrange=(MIN_RADIUS, MAX_RADIUS),
        massrange=(MIN_MASS, MAX_MASS))
sim.addPreTimeStepRunnable(adder)

sim.createCheckPointer(
        CheckPointPrms(
            fileNamePrefix='output/settle-chk',
            beginTimeStep=0,
            endTimeStep=NUM_TIMESTEPS,
            timeStepIncr=100))

sim.run()
