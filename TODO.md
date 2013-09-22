# TODO List

  * Determine how to achieve the correct bulk material properties for the ice
    shelf...
      * Density
      * Young's modulus
  * Figure out how to get the correct shape for the shelf on the scale we are
    looking at
      * Formula appears to go to zero too quickly for short shelves
      * Stretching the domain is probably cheating
  * Support simulations
      * Packing - need to let settle to de-energize bonds
      * Floating - may need to allow to come to rest before running

## Process

  1. Create a shelf mesh
  2. Run packing simulation on the mesh, record end particle positions
  3. Set up bonds and particle densities based on bulk property experiments
  4. Run buoyancy settling simulation (may be unnecessary)
  5. Run primary simulation
