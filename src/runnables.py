"""
runnables.py

Runnable modules for DEM calving simulation.
"""

from random import *
from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *

class ParticleAdder(Runnable):
    def __init__(self, sim, interval, xdomain=(-1, 1),
            ydomain=(-1, 1), zdomain=(-1, 1), radrange=(0.5, 1.5),
            massrange=(0.5, 1.5), raddist='uniform'):
        Runnable.__init__(self)
        self.sim = sim
        self.interval = interval
        self.xdomain = xdomain
        self.ydomain = ydomain
        self.zdomain = zdomain
        self.radrange = radrange
        self.massrange = massrange
        self.nextid = 0
        if raddist == 'normal':
            a, b = radrange
            mu = (a + b) / 2.0
            sigma = (b - mu) / 3.0
            self.dist = lambda a, b: normalvariate(mu, sigma)
        else:
            self.dist = lambda a, b: uniform(a, b)

    def run(self):
        if self.sim.getTimeStep() % self.interval == 0:
            self.add_particle()

    def add_particle(self):
        pos = Vec3(
                uniform(*self.xdomain),
                uniform(*self.ydomain),
                uniform(*self.zdomain))
        rad = self.dist(*self.radrange)
        mass = uniform(*self.massrange)
        p = NRotSphere(id=self.nextid, posn=pos, radius=rad, mass=mass)
        self.sim.createParticle(p)
        self.nextid += 1
