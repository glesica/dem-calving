"""
runnables.py

Runnable modules for DEM calving simulation.
"""

import sys
from random import *
from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *


class IntervalRunnable(Runnable):
    def __init__(self, sim, interval):
        Runnable.__init__(self)
        self.sim = sim
        self.interval = interval
        self.active = True

    def run(self):
        if (self.sim.getTimeStep() % self.interval == 0) and self.active:
            self.process()


class ParticleAdder(IntervalRunnable):
    def __init__(self, sim, interval, xdomain=(-1, 1),
            ydomain=(-1, 1), zdomain=(-1, 1), radrange=(0.5, 1.5),
            massrange=(0.5, 1.5), raddist='uniform', goal_particles=100):
        IntervalRunnable.__init__(self, sim, interval)
        self.xdomain = xdomain
        self.ydomain = ydomain
        self.zdomain = zdomain
        self.radrange = radrange
        self.massrange = massrange
        self.goal_particles = goal_particles
        self.nextid = 0
        if raddist == 'normal':
            a, b = radrange
            mu = (a + b) / 2.0
            sigma = (b - mu) / 3.0
            self.dist = lambda a, b: normalvariate(mu, sigma)
        else:
            self.dist = lambda a, b: uniform(a, b)

    def process(self):
        if self.nextid >= self.goal_particles:
            self.active = False
        pos = Vec3(
                uniform(*self.xdomain),
                uniform(*self.ydomain),
                uniform(*self.zdomain))
        rad = self.dist(*self.radrange)
        mass = uniform(*self.massrange)
        p = NRotSphere(id=self.nextid, posn=pos, radius=rad, mass=mass)
        self.sim.createParticle(p)
        self.nextid += 1


class EnergyLogger(IntervalRunnable):
    EPSILON = 0.0001

    def __init__(self, sim, interval):
        IntervalRunnable.__init__(self, sim, interval)

    def process(self):
        ps = self.sim.getParticleList()
        etot = sum([0.5 * p.getMass() * p.getVelocity().norm()**2 for p in ps])
        print self.sim.getTimeStep(), self.sim.getNumParticles(), etot
        if etot < self.EPSILON:
            self.sim.exit()
            sys.exit(0)
