
from base_simulation import BaseSimbox, BaseCircle, BaseRenderer
from renderers import SimDisplayer, SimExporter
# Newtons Cradle
def newtons_cradle():
    import numpy as np
    sim = BaseSimbox(radius=100, boundary_color=(255, 255, 255), boundary_thickness=1, steps_per_frame=50,
                                  amount=7,
                                  positions=[[0, -90], [0, -20], [0, -10], [0, 0], [0, 10], [0, 20], [0, 90]],
                                  sizes=[4, 4, 4, 4, 4, 4, 4],
                                  speeds=[2, 0, 0, 0, 0, 0, 0, 0],
                                  # NOTICE len(speeds) > amount,
                                  # all iterable arguments are constrained by len(arg) >= amount
                                  angles=[np.pi / 2, 0, 0, 0, 0, 0, 0],
                                  vectors=None, # vectors defined through speeds and angles. (polar form)
                                  weights=[1, 1, 1, 1, 1, 1, 1],
                                  damping=[0.0 for i in range(7)], # Must Be 0
                                  colors=[(60, 120, 250) for _ in range(7)])
    SimDisplayer(sim).run_live_sim()

# Inheriting Renderer For Displaying Info
def inherit_renderer():
    from PIL import Image, ImageDraw, ImageFont
    import random
    from extras import random_vectors_in_circle
    class InfoDisplayer(SimDisplayer):
        def render_frame(self) -> Image:
            img = super().render_frame()
            draw = ImageDraw.Draw(img)
            draw.text((img.size[0] / 40,img.size[0] / 40), f"Frame {self.simbox.current_frame}",
                      font=ImageFont.truetype('arial.ttf', size=int(img.size[0] / 40)))
            collisions_on_frame = sum([len(circle.current_colliders) for circle in self.simbox.circles])
            draw.text((img.size[0] / 40, 2 * img.size[0] / 40), f"Collisions Now {collisions_on_frame}",
                      font=ImageFont.truetype('arial.ttf', size=int(img.size[0] / 40)))
            return img
    amount = 100
    radius = 100
    boundary_color = (255, 255, 255)
    boundary_thickness = 5
    positions = random_vectors_in_circle(amount, radius)
    sizes = [3 for _ in range(amount)]
    speeds = [1 for _ in range(amount)]
    angles = [random.random() * 6.28 for _ in range(amount)]
    weights = [1 for _ in range(amount)]
    damping = [0.0 for _ in range(amount)]
    colors = [(60, 120, 250) for _ in range(amount)]
    sim = BaseSimbox(radius=radius, boundary_color=boundary_color, boundary_thickness=boundary_thickness,
                     steps_per_frame=1,
                     amount=amount, positions=positions, sizes=sizes, angles=angles, speeds=speeds, vectors=None,
                     weights=weights, damping=damping, colors=colors)

    InfoDisplayer(sim).run_live_sim()

# Spiral shape vanilla sim
def spiral_sim():
    import numpy as np, random
    amount = 140
    radius = 100
    boundary_color = (255, 255, 255)
    boundary_thickness = 5
    positions = [[(radius / (amount * 0.3)) * x * np.cos(x), (radius / (amount * 0.3)) * x * np.sin(x)] for x in np.linspace(start=10, stop=amount * 0.3, num=amount)]
    sizes = [3 for _ in range(amount)]
    speeds = [1 for _ in range(amount)]
    angles = [x for x in np.linspace(start=10, stop=amount * 0.3, num=amount)]
    weights = [1 for _ in range(amount)]
    damping = [0.0 for _ in range(amount)]
    colors = [(60, 120, 250) for _ in range(amount)]
    sim = BaseSimbox(radius=radius, boundary_color=boundary_color, boundary_thickness=boundary_thickness,
                     steps_per_frame=1,
                     amount=amount, positions=positions, sizes=sizes, angles=angles, speeds=speeds, vectors=None,
                     weights=weights, damping=damping, colors=colors)
    SimDisplayer(simbox=sim).run_live_sim()

# inheriting SimBox to add circles every time there is a collision, and randomly remove some circles on each frame
def inherit_simbox():
    import random
    from extras import random_vectors_in_circle
    class PopCornSim(BaseSimbox):
        def simulate_frame(self):
            super(PopCornSim, self).simulate_frame()
            collisions_on_frame = sum([len(circle.current_colliders) for circle in self.circles])
            positions = random_vectors_in_circle(amount=collisions_on_frame, radius=self.radius)
            vector = random_vectors_in_circle(amount=collisions_on_frame, radius=2)
            new_circles = [BaseCircle(radius=3,vector=vector[i], position=positions[i], color=(min(3 * len(self.circles), 255),min(12 * len(self.circles), 255),100)) for i in range(collisions_on_frame)]
            for i in new_circles:
                self.add_circle(i)
            for i in range(len(self.circles) // 12):
                self.circles.pop(random.randint(0, len(self.circles) - 1))
    sim = PopCornSim(radius=100, boundary_color=(10, 255, 25), boundary_thickness=10, steps_per_frame=1,
                    amount=0, positions=None, sizes=None, angles=None, speeds=None, vectors=None, weights=None,
                    damping=None, colors=None)
    for i in range(10):
        sim.add_circle(BaseCircle(radius=3, vector=random_vectors_in_circle(1, 2)[0], position=random_vectors_in_circle(1, sim.radius)[0]))
    SimDisplayer(simbox=sim).run_live_sim()

if __name__ == '__main__':
    inherit_simbox()
