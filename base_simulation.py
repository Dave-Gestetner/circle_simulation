import numpy as np
from PIL import Image, ImageDraw

class BaseRenderer:
    def __init__(self, simbox, resolution=3):
        # Resolution is the factor by which the sizes and positions are multiplied
        # Example. simulation size = 10, resolution = 20. display size will be 10*20 = 200
        self.resolution = resolution
        # simulation environment to render (instance of BaseSimbox)
        self.simbox = simbox
        # size of the screen in pixels. shape is square such that <width = height>
        self.size = int(self.resolution * self.simbox.radius * 2)

    def render_frame(self) -> Image:
        '''
        Responsible for drawing the circles onto the screen in their correct position and size
        Position: In Simbox: position range is (-simbox.radius, +simbox.radius) on x and y.
                  In renderer: position ranges from 0 <-> self.size

                  In Simbox: height increases as y increases
                  In renderer: height increases as y decreases

        Example: circle.position = [0,0]. real position = center.
        Example: circle.position = [2, - 5]. real position [center+2, center+5]

        Notice the '+' in example 2. as stated earlier, renderer and Simbox systems
        interpret increasing Y differently.
        :return: PIl.Image
        '''
        # Initialize image
        img = Image.new('RGB', size=(self.size, self.size))
        # Initialize Draw object
        draw = ImageDraw.Draw(img)

        # draw Simbox Boundaries
        draw.ellipse([0,0, self.size, self.size], outline=self.simbox.color, width=self.simbox.thickness)

        # For each circle in the simulation
        sim_center = self.simbox.radius * self.resolution
        for c in self.simbox.circles:
            # create the bounding box which decides where and at what size the circle should be drawn

            left = sim_center + (c.position[0] - c.radius) * self.resolution
            # subtract the y position from the center (-y = +y in the conversion between simbox and renderer).
            top = sim_center - (c.position[1] + c.radius) * self.resolution
            # move the entire size of the circle to the right
            right = left + 2 * c.radius * self.resolution
            # move the entire size of the circle to the bottom
            bottom = top + 2 * c.radius * self.resolution

            # draws circle defined by bounding box with color specified by circle instance
            draw.ellipse([left, top, right, bottom], fill=c.color)
        return img

    def _initialize(self):
        pass

    def close(self):
        pass

class BaseSimbox:
    def __init__(self, radius, boundary_color, boundary_thickness, steps_per_frame,
                 amount=0, positions=None, sizes=None, angles=None, speeds=None, vectors=None,
                 weights=None, damping=None, colors=None):

        self.color = boundary_color
        self.thickness = boundary_thickness

        # all circles that are part of the sim. Adding Circles while the simulation is running is allowed
        # (for future safety, use self.add_circle)
        self.circles = list()

        # radius of the simulation box. (bounded area)
        self.radius = radius

        # position set to center. useful for conforming to the way collision is handled in BaseCircle class
        self.position = np.array([0, 0], dtype=np.float64)

        # STILL UNIMPLEMENTED. a grid of which circles are near each other to even be checked for collision.
        self.grid_size = 1

        # movements and collision recalibrations per rendered frame
        self.steps_per_frame = steps_per_frame

        # keeps track of time (info var)
        self.current_frame = 0

        self.init_circles(amount=amount, positions=positions,
                          sizes=sizes, angles=angles, speeds=speeds,  weights=weights,
                          damping=damping, colors=colors, vectors=vectors)

    def init_circles(self, amount:int, positions, sizes,  angles, speeds, weights, damping, colors, vectors):
        '''
        :param amount: number of circles to simulate
        :param positions: list of size "amount" populated by
                          position vectors specifying each circles starting position
        :param sizes: list of size "amount" populated by
                      size (floats) specifying each circles radius
        :param angles: list of size "amount" of directions the circles will be travelling initially (alternatively fullfilled
                       when supplying vectors param)
        :param speeds: list of size "amount" of speeds the circles will be travelling initially (alternatively fullfilled
                       when supplying vectors param)
        :param vectors: list of size "amount" populated by
                        movement vectors specifying each circles starting velocity and angle
                        (alternatively fulfilled when supplying angles, speeds params)
        :param weights: list of size "amount" populated by
                        weight (i.e. mass) of type floats specifying each circles weight.
        :return: None
        '''
        for i in range(amount):
            try:
                if not vectors:
                    c = BaseCircle(simbox=self, name="c" + str(i), radius=sizes[i], angle=angles[i], speed=speeds[i],
                                   weight=weights[i], damping=damping[i], color=colors[i])
                else:
                    c = BaseCircle(simbox=self, name="c" + str(i), radius=sizes[i], vector=vectors[i],
                                   weight=weights[i], damping=damping[i], color=colors[i])
                c.position = np.array(positions[i], dtype=np.float64)
            except IndexError as e:
                print("All arguments must be iterables of len >= amount")
                raise e
            self.circles.append(c)

    def simulate_frame(self):
        '''
        top-level function to run a single frame of the simulation.
        (runs a full frame, potentially containing multiple sub-steps)
        :return:
        '''
        for i in range(self.steps_per_frame):
            self.current_frame += 1

            # take care of collisions
            for circle in self.circles:
                neighbors = self.get_possible_colliders(circle)
                circle.update_movement_vector(my_neighbors=neighbors)

            # move circles according to their (updated) movement vectors
            for circle in self.circles:
                circle.update_position()

            # ensures no circle escapes boundary or overlaps with another circle
            for c in self.circles:
                c._clean_collisions()

    def get_possible_colliders(self, circle):
        '''
        :param circle:
        :return: list of neighbors
        '''
        # copy all circles into new list
        colliders = self.circles.copy()
        # remove itself from the list (it cannot collide in itself)
        colliders.remove(circle)
        # add simbox as potential collider
        colliders.append(self)
        # Grid system code comes here. still unimplemented
        return colliders

    def add_circle(self, circle):
        '''
        :param circle: Circle to add to Sim
        :return:
        '''
        circle.sim_box = self
        self.circles.append(circle)

class BaseCircle:

    def __init__(self, simbox=None, name='',radius=5, weight=1, damping=0,
                 color=(156, 156, 156), angle=0, speed=0, vector=None, position=None):
        # name has no use cases so far
        self.name = name
        # color of each circle. Renderer classes use it
        self.color = color

        # simulation environment (outer circle that keeps the sim bounded)
        self.sim_box = simbox

        # circle size ( 1/2 diameter)
        self.radius = radius

        # x, y component form of a vector for movement, can be given in vector or polar form
        if vector is not None:
            self.vector = vector
        else:
            # constructs vector from standard polar to vector form equation using params "angle" and "speed"
            self.vector = speed * np.array([np.cos(angle), np.sin(angle)])

        # vector form. stores current "final" position after every sim-step
        self.position = position if position is not None else np.array([0., 0.])

        # stores temporary position, direction and speed while in the midst of sim-step
        self.temp_position = np.array([0, 0])
        self.temp_vector = np.array([0, 0])

        # weight of given circle (mass)
        self.weight = weight

        # damping co-efficient.. (the higher, the more energy lost on collision)
        self.damping = 1 - damping

        # info...
        self.number_of_collisions = 0  # total amount of collisions from inception till now
        self.distance_traveled = 0   # total distance travelled by this circle from inception till now
        self.circle_time = 0
        # more info variables may follow

        # stores a list of all colliders and is updated on every sim-step. (useful as info and for clean_collisions)
        self.current_colliders = []

    def __str__(self):
        return f"""
Name:                 {self.name}        
Speed:                {np.linalg.norm(self.vector)}
Angle:                {self._vector_angle()}
Position              {self.position}  
Number-of-collisions: {self.number_of_collisions}
Total Distance:       {self.distance_traveled}
"""

    def update_movement_vector(self, my_neighbors):
        '''
        top level function to take care of collisions. (calls self._handle_collision, self._handle_simbox_collision
        for the heavy lifting)
        :param my_neighbors: all circles in the simulation environment (simbox) + the simbox's walls
        :return: None
        '''
        # ensures constant time no matter simbox steps per frame
        self.circle_time += 1 / self.sim_box.steps_per_frame
        # get all circles colliding with self
        self.current_colliders = self._is_colliding_with(neighbors=my_neighbors)

        # copy current vector, position explicitly to temporary (in case there are no collisions)
        self.temp_vector = self.vector.copy()
        self.temp_position = self.position.copy()

        # handle vector changes due to collisions
        for collider in self.current_colliders:
            # if self collided with the wall..
            if isinstance(collider, BaseSimbox):
                self._handle_simbox_collision()

            # if self collided with another circle..
            else:
                self._handle_collision(collider)

    def update_position(self):
        '''
        simulates the movement of the circles by moving their position based on self.vector
        :return:
        '''
        self.position = self.temp_position
        self.vector = self.temp_vector

        self.position += self.vector / self.sim_box.steps_per_frame

        # add the magnitude of the vector to the distance_traveled info variable
        self.distance_traveled += abs(np.linalg.norm(self.vector))

        # reset the temporary variables to nothing (not needed. just a safety feature...)
        self.temp_vector = np.array([0,0])
        self.temp_position = np.array([0,0])

    def _handle_collision(self, collider):
        '''
        :param collider: BaseCircle instance that collides with self
        handles the vector changes after a collision. "the gut of the simulation".
        self.vector is changed to transfer (some of) its momentum to colliding circles.
        Each circle involved in the collision is updated on separate calls.
        :return:
        '''

        d = np.sqrt((self.temp_position[0] - collider.position[0]) ** 2 + (self.temp_position[1] - collider.position[1]) ** 2)
        norm_x = (self.temp_position[0] - collider.position[0]) / d
        norm_y = (self.temp_position[1] - collider.position[1]) / d

        p = 2 * (self.temp_vector[0] * norm_x + self.temp_vector[1] * norm_y - collider.vector[0] * norm_x - collider.vector[1] * norm_y) / (self.weight + collider.weight)

        self.temp_vector[0] = self.temp_vector[0] - p * norm_x * collider.weight
        self.temp_vector[1] = self.temp_vector[1] - p * norm_y * collider.weight
        self.temp_vector *= self.damping

    def _handle_simbox_collision(self):
        '''
        Different then reg collision, as no momentum is transferred into the simbox.
        [Its a collider body, not a rigid body, in c4d lingo...]
        :return:None
        '''
        # reflect vector over position vector
        posit_normalized = self.position / np.linalg.norm(self.position)
        proj = (np.dot(self.temp_vector, posit_normalized) / np.dot(posit_normalized, posit_normalized)) * posit_normalized
        self.temp_vector = self.temp_vector - 2 * proj

    def _clean_collisions(self):
        '''
        creates distance between each colliding circle, enough to take it out of range. so that it wont look strange
        :return: None
        '''
        for collider in self.current_colliders:
            cur_distance = np.linalg.norm(self.position - collider.position)
            # colliding with boundary
            if isinstance(collider, BaseSimbox):
                max_distance = collider.radius - self.radius
                if cur_distance > max_distance:
                    self.position = (max_distance / cur_distance) * self.position

            else:
                min_distance = self.radius + collider.radius
                if min_distance - cur_distance > 0:
                    difference = (min_distance - cur_distance) * (collider.position - self.position)
                    self.position = self.position - difference

    def _is_colliding_with(self, neighbors)->list:
        '''
        :param neighbors: Possible colliders list received from simbox. at this point, it includes all circles in the
        sim, and the simbox
        :return: list of colliding neighbors
        '''
        colliders = []
        for n in neighbors:
            # measures distance from n
            # magnitude of vector a - b = direct line..
            cur_distance = np.linalg.norm(self.position - n.position)
            # if n is another circle..
            if not isinstance(n, BaseSimbox):
                # Test if they collide with each other; test works by calculating the closest (closest=furthest) they
                # can to be without colliding, and checking if cur_distance < allowed_distance.
                if cur_distance <= self.radius + n.radius:
                    self.number_of_collisions += 1
                    colliders.append(n)

            # else, if n is the simbox-wall
            else:
                # if cur_distance > allowed_distance -> [radius of simulation-box]
                if cur_distance >= self.sim_box.radius - self.radius:
                    colliders.append(n)

        return colliders

    def _vector_angle(self):
        '''
        gets the angle-component from a vector
        :return: angle
        '''
        # check for edge case when there is no magnitude in vector which results in a zero division error
        angle = np.pi / 2 if self.vector[0] == 0 else np.arctan(self.vector[1] / self.vector[0])
        # if the angle is in quads 2,3. which makes the x-component negative
        if self.vector[0] < 0:
            # spin the angle by 2 quads.. so 1->3, 4->2
            angle = angle + np.pi
        return angle



