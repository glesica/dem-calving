# DEM Calving Simulation

A Discrete Element Method ice sheet calving simulation. This is a
work-in-progress. In addition to the model itself, the plan is to implement
several support simulations for parameterization of the model and particle
packing.

## Basic Instructions

  1) Install ESyS-Particle (see:
     https://answers.launchpad.net/esys-particle/+faq/1613) - note that only the
     2.2 series will work (2.2.2 is known to work)
  2) Run a simulation (right now only the packing simulation exists): `./run.sh
     packer 100000` (for 100000 timesteps)
