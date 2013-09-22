"""
mesh.py

Script to create meshes from templates.
"""

import sys
from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('src/meshes/templates/'))

def load_template(f):
    """
    Load the mesh template with name f.
    """
    return ENV.get_template(f)

def render_template(f, **kwargs):
    """
    Render the template with name f using the provided keyword arguments.
    """
    return load_template(f).render(**kwargs)

def cuboid(xdim, ydim, zdim):
    """
    Render a cuboid mesh template using the provided dimensions.
    """
    return render_template('cuboid.msh', xdim=xdim, ydim=ydim, zdim=zdim)

if __name__ == '__main__':
    meshname = sys.argv[1]
    if meshname == 'cuboid':
        mesh = cuboid(*sys.argv[3:])
    outpath = sys.argv[2]
    with open(outpath, 'w') as f:
        f.write(mesh)
