# Circle Simulation
### A Bouncing Circles Versatile Physics Simulator Implemented In Python.
This is a compact basic simulation package in which circles bounce around in a bounded area and collide with each other to make
for a satisfying visual effect. The package is designed to be simple to use, allowing users to customize parameters like the number of circles, their speed, size, mass, restitution (damping) and the boundaries of the simulation. It can serve as a foundation for further building of physics-based simulations involving gravity, attractors and other forces or as a physics simulation playground in which interesting setups and modifications can give rise to interesting results.

The package gives a wide degree of freedom to the user in modifying the existing simulation-classes by taking advantage of inheritance. it is easy to use, with multiple examples that explore the usage and customization of the code (see Examples.py). It also includes a robust testing module which can also be used to explore the various parameters and options available.

### Enjoy💣

## Installation
`pip install git+https://github.com/Dave-Gestetner/circle_simulation.git`

or clone and set up by yourself by following these steps.
1. Navigate to the installation folder
2. run `git clone https://github.com/Dave-Gestetner/circle_simulation.git`
3. navigate to circle_simulation
4. run `python setup.py install`

then run **setup.py**

## Usage
There are 3 basic classes that, together form the foundation of everything you will build.
+ BaseCircle
+ BaseSimbox
+ BaseRenderer

To import them, type `from circle_simulation.base_simulation import BaseCircle, BaseSimbox, BaseRenderer`

### Classes

**BaseCircle** defines the circles that make up the objects in the simulation. It has properties such as *position*, *radius* (size)
, *weight* (mass), *color* etc.

**BaseSimbox** defines the simulation-scene and it stores a list of BaseCircles (or its subclasses) as the particles. It has properties such as *steps_per_frame*, *radius*(scene size), "boundary_thickness", and *current_frame* (simulation time) etc.

**BaseRenderer** defines how to render the simulation data onto a image and uses PIL to do so. It has properties such as *resolution* and is mostly used as a superclass and not as a standalone. (see SimDisplayer and SimExporter)

**SimDisplayer** and **SimExporter** can be imported using 
`from circle_simultion.renderers import SimDisplayer, SimExporter`

**SimDisplayer** is a subclass of *BaseRenderer* and is used to display the simulation, live on screen. It uses Pygame for the live display and allows to set *fps*.
It can also be inherited to add more functionality to it. (see Examples.py inherit_renderer())

### Example
```
from circle_simulation.base_simulation import BaseSimbox, BaseCircle
from circle_simulation.renderers import SimDisplayer

particle = BaseCircle(color=(255, 155, 105), angle=3.142 / 3, speed=5)
scene = BaseSimbox(radius=100, boundary_color=(90, 45, 35), boundary_thickness=3, steps_per_frame=1, amount=0)
scene.add_circle(particle)
SimDisplayer(simbox=scene, resolution=5, fps=30).run_live_sim()
```

Result will be one circle bouncing from wall to wall. This is the simplest scene possible, now go ahead and add more particles, mess around with their parameters and have fun!



Follow me on [Linkedin](https://www.linkedin.com/in/dave-g-026b142aa/)

